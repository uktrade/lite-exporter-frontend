@login @all
Feature: I want to be able to login and logout of LITE
  As a exporter
  I want to be able to login to LITE
  So that I can see my exporter dashboard

  @reg
  Scenario: Register a new user
    Given I create a new user

  @LT_1134_valid @regression
  Scenario: Login with valid credentials
    Given I go to exporter homepage and choose Test Org
    Then page title equals "Exporter hub - LITE - GOV.UK"

  @LT_1467_logout @regression
  Scenario: Logout of LITE
    Given I go to exporter homepage and choose Test Org
    When I click the logout link
    Then I am taken to the GREAT.GOV.UK page
