@users @all
Feature: I want to manage users
  As a logged in exporter
  I want to manage users
  So that an application/query can be managed by only active members of staff and new members of staff can be added and their details can be kept up to date

  @LT_937_setup
  Scenario: Set up user
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    Then I add a user

  @add_user
  Scenario: Add user
    Given I go to exporter homepage and choose Test Org
    When I add user
    Then user is added

  @cant_add_self
  Scenario: Cant add own user
    Given I go to exporter homepage and choose Test Org
    When I add self
    Then error message is "is already a member of this organisation"

  @edit_user
  Scenario: Edit user
    Given I go to exporter homepage and choose Test Org
    When I edit user then user is edited

#  @deactivate
#  Scenario: Deactivate user
#    Given I go to exporter homepage and choose Test Org
#    When I add the second test user
#    And I deactivate user then user is deactivated
#    And I go to exporter homepage
#    And I reactivate user then user is reactivated

  @reactivate_oneself
  Scenario: Reactivate oneself
    Given I go to exporter homepage and choose Test Org
    When I try to deactivate myself I cannot
