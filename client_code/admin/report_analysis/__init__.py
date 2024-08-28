from ._anvil_designer import report_analysisTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import anvil.server
import re  # Import the regular expression module

class report_analysis(report_analysisTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user
        if user is not None:
            self.label_656.text = user['user_fullname']
        
        # Hide plot initially
        self.plot_1.visible = False
        self.refresh_data("transaction_trends")
      
    def refresh_data(self, data_type):
        if data_type == "transaction_trends":
            # Call the server function to get transactions data
            transactions = anvil.server.call('get_transactions', self.user['user_fullname'])
        
            # Organize data for plotting (example: aggregate by date and type)
            data_for_plot = {}
            for transaction in transactions:
                date = transaction['transaction_timestamp']
                trans_type = transaction['transaction_type']
                fund = transaction['transaction_amount']  # Retrieve the 'fund' field
        
                if date not in data_for_plot:
                    data_for_plot[date] = {'Debit': 0, 'Credit': 0, 'Account to G-wallet': 0}
        
                # Ensure fund is a string or a number before conversion
                if isinstance(fund, (int, float)):
                    money_amount = fund
                elif isinstance(fund, str):
                    # Extract numeric value from the 'fund' field
                    try:
                        money_amount = float(re.sub(r'[^\d.]', '', fund))
                    except ValueError:
                        money_amount = 0  # Handle cases where conversion to float fails
                else:
                    money_amount = 0  # Default to 0 if 'fund' is neither a string nor a number
        
                if trans_type == 'Debit':
                    data_for_plot[date]['Debit'] += money_amount
                elif trans_type == 'Credit':
                    data_for_plot[date]['Credit'] += money_amount
                elif trans_type == 'Account to G-wallet':
                    data_for_plot[date]['Account to G-wallet'] += money_amount
        
            # Prepare data for the plot
            categories = list(data_for_plot.keys())
            debit_values = [data['Debit'] for data in data_for_plot.values()]
            credit_values = [data['Credit'] for data in data_for_plot.values()]
            e_wallet_values = [data['Account to G-wallet'] for data in data_for_plot.values()]
        
            self.plot_1.data = [
                {'x': categories, 'y': debit_values, 'type': 'bar', 'name': 'Debit'},
                {'x': categories, 'y': credit_values, 'type': 'bar', 'name': 'Credit'},
                {'x': categories, 'y': e_wallet_values, 'type': 'bar', 'name': 'Account to G-wallet'}
            ]
            self.plot_1.layout = go.Layout(title="Transaction Trends")
        
        elif data_type == "user_activity":
            # Call the server function to get user data
            users = anvil.server.call('get_user_data')
        
            # Count the number of active, inactive, and banned users
            active_users = sum(1 for user in users if not user['inactive'] and not user['banned'])
            inactive_users = sum(1 for user in users if user['inactive'] and not user['banned'])
            banned_users = sum(1 for user in users if user['banned'])
        
            # Calculate the total number of users
            total_users = banned_users + active_users + inactive_users
        
            # Check if the total number of users is greater than zero to avoid division by zero
            if total_users > 0:
                banned_percentage = (banned_users / total_users) * 100
                active_percentage = (active_users / total_users) * 100
                inactive_percentage = (inactive_users / total_users) * 100
            else:
                # If there are no users, set percentages to zero
                banned_percentage = 0
                active_percentage = 0
                inactive_percentage = 0
        
            # Create pie chart data with labels and percentages
            labels = ['Banned Users', 'Active Users', 'Inactive Users']
            values = [banned_percentage, active_percentage, inactive_percentage]
        
            # Plot the pie chart with labels and percentages
            self.plot_1.data = [{
                'labels': labels,
                'values': values,
                'type': 'pie',
                'textinfo': 'label+percent',  # Show both label and percentage on the chart
                'hoverinfo': 'label+percent+value'  # Display value on hover for better insights
            }]
            self.plot_1.layout = go.Layout(
                title="User Activity",
                showlegend=True  # Ensure that the legend is shown
            )

        elif data_type == "system_performance":
            # Call the server function to get transaction proof data
            transaction_proofs = anvil.server.call('get_transaction_proofs')

            # Count the number of successful and failed transactions
            successful_transactions = sum(1 for proof in transaction_proofs if proof['users_transaction_status'] == 'success')
            failed_transactions = sum(1 for proof in transaction_proofs if proof['users_transaction_status'] == 'failed')

            # Calculate percentages
            total_transactions = successful_transactions + failed_transactions
            if total_transactions > 0:
                success_percentage = (successful_transactions / total_transactions) * 100
                failed_percentage = (failed_transactions / total_transactions) * 100
            else:
                success_percentage = 0
                failed_percentage = 0

            # Create pie chart data with labels and percentages
            labels = ['Successful Transactions', 'Failed Transactions']
            values = [success_percentage, failed_percentage]

            self.plot_1.data = [{
                'labels': labels,
                'values': values,
                'type': 'pie',
                'textinfo': 'label+percent',  # Show both label and percentage on the chart
                'hoverinfo': 'label+percent+value'  # Display value on hover for better insights
            }]
            self.plot_1.layout = go.Layout(
                title="System Performance",
                showlegend=True  # Ensure that the legend is shown
            )

        # Show the plot
        self.plot_1.visible = True

    def link_44_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.refresh_data("transaction_trends")

    def link_66_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.refresh_data("user_activity")

    # def link_99_click(self, **event_args):
    #     """This method is called when the button is clicked"""
    #     self.refresh_data("system_performance")

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.report_analysis', user=self.user)

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.account_management', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.transaction_monitoring', user=self.user)

    def link_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.admin_add_user', user=self.user)

    def link_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.audit_trail', user=self.user)

    def link_4_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.admin_add_user', user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        show_users_form = open_form('admin.transaction_monitoring', user=self.user)

    def link_8_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def button_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')

    def button_3_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin', user=self.user)

    def link_8_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.add_currency', user=self.user)

    def link_5_copy_click(self, **event_args):
        if self.user['users_usertype'] == 'super_admin':
            open_form('admin.manage_privacy', user=self.user)
        else:
            alert("Access Denied!")

    def link_6_copy_click(self, **event_args):
        if self.user['users_usertype'] == 'super_admin':
            open_form('admin.manage_privacy', user=self.user)
        else:
            alert("Access Denied!")