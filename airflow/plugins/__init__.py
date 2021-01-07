from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import myoperators

# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "udacity_plugin"
    operators = [
        myoperators.StageToRedshiftOperator,
        myoperators.LoadFactOperator,
        myoperators.LoadDimensionOperator,
        myoperators.DataQualityOperator
    ]
   
