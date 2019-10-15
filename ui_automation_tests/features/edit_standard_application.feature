@licence @edit @all @standard
Feature: I want to be able to edit and update an active application
  As a logged in exporter
  I want to be able to edit and update an active application
  So that any additional information and/or corrected details can be updated on my application

  @LT_998_edit_application
  @ECF
  Scenario: Edit a standard application
    Given I go to exporter homepage and choose Test Org
    And a standard application exists
    When I click on applications
    And I click on application previously created
    And I click edit application
    And I remove all goods on the application
    Then No goods are left on the application
    When I remove the end user off the application
    Then No end user is set on the application
