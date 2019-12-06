@users @all
Feature: I want to manage users
  As a logged in exporter
  I want to manage users
  So that an application/query can be managed by only active members of staff and new members of staff can be added and their details can be kept up to date

  @LT_937_setup @smoke
  Scenario: Set up user
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    Then I add a user

  @add_user @regression
  Scenario: Add user, then deactivate and reactivate them
    Given I go to exporter homepage and choose Test Org
    When I add user
    Then user is added
    When I deactivate user then user is deactivated
    And I reactivate user then user is reactivated

  @cant_add_self @regression
  Scenario: Can't add own user
    Given I go to exporter homepage and choose Test Org
    When I add self
    Then error message is "is already a member of this organisation"

  @reactivate_oneself @regression
  Scenario: Reactivate oneself
    Given I go to exporter homepage and choose Test Org
    When I try to deactivate myself I cannot
