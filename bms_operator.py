from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults
import os
import urllib.request
from bs4 import BeautifulSoup
import re

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)


class BMSOperator(BaseOperator):
    """
    Check availability of a movie in given list of venues

    :param site_url: url of movie page on bms
    :type site_url: str
    :param date: date for tickets search
    :type date: str
    :param venue: venue for tickets search
    :type venue: str
    """

    @apply_defaults
    def __init__(self,
                 site_url,
                 show_date,
                 venue,
                 *args,
                 **kwargs):
        super(BMSOperator, self).__init__(*args, **kwargs)
        self.site_url = site_url
        self.show_date = show_date
        self.venue = venue

    def execute(self, context):
        """
        Checking the site page for given list of venues
        """

        url = self.site_url + self.show_date

        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find_all('div', {'data-online': 'Y'})
        line = str(soup)
        soup = BeautifulSoup(line, 'lxml')
        soup = soup.find_all('a', {'data-venue-code': self.venue})
        line = str(soup)
        result = re.findall('data-availability="A"', line)
        if len(result) > 0:
            print("Available at " + self.venue)
        else:
            raise Exception("No tickets available yet at " + self.venue)

class BMSOperatorPlugin(AirflowPlugin):
    name = "bms_operator"
    operators = [BMSOperator]

# # Self Test
# if __name__ == "__main__":
#     a = BMSOperator(site_url="https://in.bookmyshow.com/buytickets/avengers-infinity-war-3d-bengaluru/movie-bang-ET00074502-MT/", date="20180427", venue='INMB', task_id="self_test")
#     a.execute({})
