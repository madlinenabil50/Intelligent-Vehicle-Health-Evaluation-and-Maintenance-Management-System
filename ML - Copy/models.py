import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers, initializers

def build_optimized_lstm(input_shape):
    """
    [3A] Optimized LSTM for Time-Series Regression:
    - Unidirectional LSTM to prevent data leakage (no future info)
    - 3 LSTM layers with increasing dropout and recurrent dropout for stability
    - Batch Normalization after each LSTM layer
    - L2 Regularization to reduce overfitting
    - Gradient clipping applied during training (handled in train.py)
    - Improved initialization for better convergence
    """
    model = models.Sequential([
        # Input layer
        layers.Input(shape=input_shape),
        
        # Layer 1: LSTM with high capacity, moderate regularization
        layers.LSTM(128, return_sequences=True, 
                   kernel_regularizer=regularizers.l2(0.001),
                   recurrent_regularizer=regularizers.l2(0.001),
                   kernel_initializer=initializers.GlorotUniform(seed=SEED),
                   recurrent_initializer=initializers.Orthogonal(seed=SEED)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),  # Increased dropout
        
        # Layer 2: Reduced capacity, higher dropout
        layers.LSTM(64, return_sequences=True, 
                   kernel_regularizer=regularizers.l2(0.001),
                   recurrent_regularizer=regularizers.l2(0.001),
                   kernel_initializer=initializers.GlorotUniform(seed=SEED),
                   recurrent_initializer=initializers.Orthogonal(seed=SEED)),
        layers.BatchNormalization(),
        layers.Dropout(0.4),  # Higher dropout for stability
        
        # Layer 3: Final LSTM, no return sequences
        layers.LSTM(32, 
                   kernel_regularizer=regularizers.l2(0.001),
                   recurrent_regularizer=regularizers.l2(0.001),
                   kernel_initializer=initializers.GlorotUniform(seed=SEED),
                   recurrent_initializer=initializers.Orthogonal(seed=SEED)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        
        # Dense layers with regularization
        layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001),
                    kernel_initializer=initializers.GlorotUniform(seed=SEED)),
        layers.Dropout(0.2),
        layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.001),
                    kernel_initializer=initializers.GlorotUniform(seed=SEED)),
        layers.Dropout(0.2),
        layers.Dense(1, activation='linear', kernel_initializer=initializers.GlorotUniform(seed=SEED))  # Regression Output
    ])
    
    return model

def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0.1):
    """
    Transformer Encoder Block with improvements:
    - Pre-LayerNorm for stability
    - Residual connections
    - Tuned dropout
    - Feed-forward with GELU activation for better performance
    """
    # Attention with residual
    x = layers.LayerNormalization(epsilon=1e-6)(inputs)
    attn_output = layers.MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(x, x)
    attn_output = layers.Dropout(dropout)(attn_output)
    x = attn_output + inputs  # Residual
    
    # Feed Forward with residual
    x_norm = layers.LayerNormalization(epsilon=1e-6)(x)
    ff_output = layers.Conv1D(filters=ff_dim, kernel_size=1, activation="gelu")(x_norm)  # GELU for better grad flow
    ff_output = layers.Dropout(dropout)(ff_output)
    ff_output = layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(ff_output)
    return ff_output + x  # Residual

class PositionalEncoding(layers.Layer):
    """
    Fixed Positional Encoding:
    - Corrected np.cast to np.float32
    - Ensures compatibility with TensorFlow
    """
    def __init__(self, sequence_length, d_model):
        super(PositionalEncoding, self).__init__()
        self.pos_encoding = self.positional_encoding(sequence_length, d_model)

    def get_angles(self, pos, i, d_model):
        angles = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))  # Fixed: np.cast -> np.float32
        return pos * angles

    def positional_encoding(self, position, d_model):
        angle_rads = self.get_angles(np.arange(position)[:, np.newaxis],
                                    np.arange(d_model)[np.newaxis, :],
                                    d_model)
        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
        pos_encoding = angle_rads[np.newaxis, ...]
        return tf.cast(pos_encoding, dtype=tf.float32)

    def call(self, inputs):
        # Slice to match input sequence length dynamically
        seq_len = tf.shape(inputs)[1]
        return inputs + self.pos_encoding[:, :seq_len, :]

def build_optimized_transformer(input_shape):
    """
    [3B] Optimized Transformer for Time-Series Regression:
    - Positional Encoding fixed and applied correctly
    - Multiple encoder blocks for deeper representation
    - Improved attention with larger head_size and more heads
    - Better dropout strategy (0.1-0.2)
    - L2 Regularization on dense layers
    - Global pooling to handle variable sequence lengths
    - GELU activation in feed-forward for smoother gradients
    """
    inputs = layers.Input(shape=input_shape)
    
    # Positional Encoding
    x = PositionalEncoding(input_shape[0], input_shape[1])(inputs)
    
    # Multiple Transformer Encoder Blocks (increased to 4 for better performance)
    x = transformer_encoder(x, head_size=256, num_heads=8, ff_dim=128, dropout=0.1)  # Larger head_size
    x = transformer_encoder(x, head_size=256, num_heads=8, ff_dim=128, dropout=0.1)
    x = transformer_encoder(x, head_size=256, num_heads=8, ff_dim=128, dropout=0.15)
    x = transformer_encoder(x, head_size=256, num_heads=8, ff_dim=128, dropout=0.2)
    
    # Global Pooling to convert sequence to vector
    x = layers.GlobalAveragePooling1D(data_format="channels_last")(x)
    
    # Output Layers with regularization and dropout
    x = layers.Dense(128, activation="gelu", kernel_regularizer=regularizers.l2(0.001),
                    kernel_initializer=initializers.GlorotUniform(seed=SEED))(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(64, activation="gelu", kernel_regularizer=regularizers.l2(0.001),
                    kernel_initializer=initializers.GlorotUniform(seed=SEED))(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(1, activation="linear", kernel_initializer=initializers.GlorotUniform(seed=SEED))(x)
    
    return models.Model(inputs, outputs)