from sqlalchemy.orm import as_declarative, declared_attr


# using declarative style
@as_declarative()
class Base:
    __name__: str

    # generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        is_second_supper: bool = False
        index_second_supper: int = 1
        for i in range(1, len(self.__name__)):
            if self.__name__[i].isupper():
                is_second_supper = True
                index_second_supper = i
                break

        if is_second_supper:
            return (self.__name__[:index_second_supper] + '_' + self.__name__[index_second_supper:]).lower()
        return self.__name__.lower()
