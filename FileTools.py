import os


class DirFileManager:

    def __init__(self, file: str = "a.out", mode: str = 'ab', dir_name: str = "stuff"):
        self.files = 0

        self._n = file
        self.__dir_name = dir_name
        self.__mode = mode
        self.__current_file = os.getcwd()  # 获取运行文件当前相对路径

        self.__dir_path = os.path.abspath(self.__current_file).replace(self.__current_file,
                                                                       self.__dir_name)  # 获取新文件夹绝对目录

        self.__file = None
        self.__file_path = None

        self.__create_dir()  # 创建新文件夹
        self.create_new_file(file)  # 在文件夹中创建新文件

        if 'r' in self.__mode:
            raise ReadError

    def __create_dir(self):
        """it creates a dir"""
        try:
            os.mkdir(self.__dir_path)
        except FileExistsError:
            pass

    def create_new_file(self, file_name=None):
        """it creates a new file and close another one"""
        try:
            self.__file.close()
        except AttributeError:
            pass

        if file_name is None:
            file_name = self._n

        self.files += 1

        name = f"{file_name.split('.')[0]}({self.files}).{file_name.split('.')[1]}"
        self.__file_path = f"{self.__dir_path}\\{name}"
        self.__file = open(self.__file_path, self.__mode)

    def write(self, msg):
        self.__file.write(msg)

    def read(self):
        return self.__file.read()

    def readlines(self):
        return self.__file.readlines()

    def close(self):
        self.__file.close()

    @property
    def abs_path(self):
        """it returns the path of the file"""
        return self.__file_path

    @property
    def dir_name(self):
        return self.__dir_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file.close()


class ReadError(Exception):
    pass


if __name__ == '__main__':
    # unit test
    fd = DirFileManager(mode='w')
    fd.write("No.1")
    fd.create_new_file('a.out')
    fd.write("No.2")
