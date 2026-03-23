from river import linear_model, preprocessing, compose, feature_extraction

def get_online_model():
    """
    Returns a River pipeline for online classification.
    Handles categorical features (protocol_type, service, flag) using One-Hot Encoding.
    """
    model = (
        compose.SelectType(int, float) | preprocessing.StandardScaler()
    )
    model += (
        compose.SelectType(str) | preprocessing.OneHotEncoder()
    )
    model |= linear_model.LogisticRegression()
    
    return model
