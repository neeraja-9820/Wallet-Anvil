from ._anvil_designer import notification_serviceTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class notification_service(notification_serviceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.user = user
    # self.label_1.text=self.user['user_fullname']
    self.hide_all_panels()
  def hide_all_panels(self):
    self.column_panel_1.visible = False
    self.column_panel_2.visible = False
    self.column_panel_3.visible = False
    self.column_panel_4.visible = False
    self.column_panel_5.visible = False
    self.column_panel_6.visible = False
    # Add more panels if you have more column panels










  def link_8_copy_click(self, **event_args):
    open_form('admin', user=self.user)

  def link_8_click(self, **event_args):
    open_form('admin', user=self.user)

  def link_20_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.notification_service', user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management', user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring', user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.admin_add_user', user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail', user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.user_support', user=self.user)

  def link_6_copy_2_click(self, **event_args):
    if self.user['users_usertype'] == 'super admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
    else:
          # Show an alert if the user is not a super admin
         alert("You're not a super admin. Only super admins can perform this action.")

  def link_6_copy_3_click(self, **event_args):
    open_form("admin.add_currency", user=self.user)

  def link_6_copy_4_click(self, **event_args):
    open_form("admin.add_bank_account", user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis', user=self.user)
