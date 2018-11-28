from systems.tokens.token import Token

def redeemToken(tokenHash):
    from systems.exceptions import InvalidTokenError
    token = Token.get({"token" : tokenHash})
    if not token:
        raise InvalidTokenError("The token provided is invalid")
    subject = token.subject
    action = getattr(subject, token.action)
    action()
    token.delete()