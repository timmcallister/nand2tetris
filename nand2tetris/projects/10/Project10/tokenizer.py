class JackTokenizer:

    def __init__(self, file_name):
        import re
        with open(file_name, 'r') as input_file:
            self.current_command = -1
            self.command_list = input_file.readlines()

            COMMENTS = re.compile(r'''
                                    (//[^\n]*(?:\n|$))    # My favorite part about regex
                                    |                     # is that
                                    (/\*.*?\*/)           # it's all so easy to read
                                   ''', re.VERBOSE | re.MULTILINE)

            self.command_list = COMMENTS.sub('\n', ''.join(self.command_list)).split('\n')
            self.command_list = [x.strip() for x in self.command_list]
            self.command_list = list(filter(lambda x: x != '',
                                            self.command_list))
    
    def has_more_tokens(self):
        pass

    def advance(self):
        pass

    def token_type(self):
        pass

    def key_word(self):
        pass

    def symbol(self):
        pass

    def identifier(self):
        pass

    def int_val(self):
        pass
    
    def string_val(self):
        pass

        