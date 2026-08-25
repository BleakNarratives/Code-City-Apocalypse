# TEST FILE: Designed to be an absolute architectural nightmare
import os

PASSWORD = "super_secret_api_token_123" # Smell: Security Leak

def monstrous_function_with_way_too_many_arguments(a, b, c, d, e, f, g): # Smell: Long Parameter List
    print("Testing parameters")
    # TODO: Fix this garbage code later # Smell: Hoarder Tendencies
    # FIXME: Seriously, delete this
    if a > b:
        if b > c:
            if c > d:
                if d > e:
                    print("We have reached maximum nesting depth!") # Smell: Arrow Complexity
    try:
        x = 1 / 0
    except:
        pass # Smell: Silent Killer
