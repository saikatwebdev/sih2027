MIN_PERSON_CONFIDENCE = 0.60
MIN_OBJECT_CONFIDENCE = 0.60


def valid_confidence(value, threshold):

    return value >= threshold