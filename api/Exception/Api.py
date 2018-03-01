class Api(Exception):
    def __init__(self,message,error_exception=None):
        self.error_exception = None

        if error_exception:
            self.error_exception = error_exception

        super(Api,self).__init__(message)
