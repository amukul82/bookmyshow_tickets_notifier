from airflow.operators.email_operator import EmailOperator
from airflow.operators.bms_operator import BMSOperator
from airflow.utils.trigger_rule import TriggerRule

from airflow import DAG

from datetime import datetime

default_args = {
    'start_date': datetime.strptime('2018-03-07', '%Y-%m-%d'),
}

infinity_war_ticket_check_dag = DAG(
    'infinity_war_ticket_check_dag',
    default_args=default_args,
    catchup=False,
    schedule_interval=None,
    max_active_runs=1
)

t_0 = BMSOperator(
    dag=infinity_war_ticket_check_dag,
    task_id="check_tickets_for_inox_mantri_imax",
    site_url="https://in.bookmyshow.com/buytickets/avengers-infinity-war-3d-bengaluru/movie-bang-ET00074502-MT/",
    show_date="20180427",
    venue="INMB"
)

t_1 = EmailOperator(
    dag=infinity_war_ticket_check_dag,
    task_id='email_for_inox_mantri_imax',
    trigger_rule=TriggerRule.ALL_SUCCESS,
    to='amukul82@gmail.com',
    subject='Tickets available at INOX Mantri Mall for Avengers Infinity war',
    html_content='Tickets available at INOX Mantri Mall for Avengers Infinity war'
)

t_1.set_upstream(t_0)
