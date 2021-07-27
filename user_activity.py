from models import UserActivity

class UserActivityRepository(BaseRepository):
    """
    This repository takes care of accessing runing SQL queries
    and retrieving results.
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def get(self, date):
        """
        Responsibly for selecting the user activities from the database.
        """
        return UserActivity.query().where(date=date, user_id=self.user_id)

class UserActivityTracker(object):
    """
    This class is the business logic.
    """
    def __init__(self, user_id):
        """
        Initialize the repository injecting the user_id from the app context
        """
        self.repository = UserActivityRepository(user_id=user_id)

    def get_user_activities(self, client_id, date):
        """
        This class takes care of accessing runing SQL queries
        and retrieving results
        """
        return [{'user_id': i.user_id, 'activity': i.activity_id}
                for i in self.repository.get_user_activities(date=date)
                if i.client_id == client_id]

