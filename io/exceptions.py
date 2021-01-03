class MissingEnvironmentVariable(Exception):
    def __init__(self, env):
        super().__init__(f"ENV: \"{env}\" is null but required.")
