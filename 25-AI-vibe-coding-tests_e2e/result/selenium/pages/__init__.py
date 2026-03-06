# Page Object Model classes for Flask Blog Admin UI
from .base_page import BasePage
from .statistics_page import StatisticsPage
from .users_page import UsersPage
from .posts_page import PostsPage

__all__ = ['BasePage', 'StatisticsPage', 'UsersPage', 'PostsPage']
