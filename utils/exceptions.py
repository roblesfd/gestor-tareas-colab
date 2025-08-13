

class UserNotFoundError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class TaskAlreadyExistsError(Exception):
    pass

class TaskNotCreatedError(Exception):
    pass

class TaskNotFoundError(Exception):
    pass

class TaskNotUpdatedError(Exception):
    pass

class TaskNotDeletedError(Exception):
    pass