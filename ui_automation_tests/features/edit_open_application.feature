@licence @edit @all @open
Feature: I want to be able to edit and update an active application
  As a logged in exporter
  I want to be able to edit and update an active application
  So that any additional information and/or corrected details can be updated on my application

  @LT_998_edit_application
  Scenario: Edit an open application
    Given I go to exporter homepage and choose Test Org
    And I create an open application via api
    Then no goods types are left on the application
    When I click on applications
    And I click on application previously created
    And I click edit application
    And I choose to make minor edits
    And I remove all goods types on the application
    Then no goods types are left on the application
