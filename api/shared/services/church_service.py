
from api.shared.daos.church_dao import ChurchDao


class ChurchService():
    """Church service"""
    
    def __init__(self) -> None:
        """initializes church service"""
        self.church_dao = ChurchDao()
    
    def get_all_churches(self):
        """return all churches"""
        churches = self.church_dao.get_all()
        church_list = list(map(lambda church: church.to_dict(), churches))
        return church_list
