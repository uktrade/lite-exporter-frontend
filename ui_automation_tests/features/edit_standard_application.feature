@licence @edit @all @standard
Feature: I want to be able to edit and update an active application
  As a logged in exporter
  I want to be able to edit and update an active application
  So that any additional information and/or corrected details can be updated on my application

  @LT_998_edit_application @AT
  Scenario: Edit a standard application
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    When I click on applications
    And I click on application previously created
    And I click edit application
    And I choose to make major edits
    And I click on the application goods link
    And I remove all goods on the application
    Then no goods are left on the application
    When I click back to the application overview
    And I remove the end user off the application
    Then no end user is set on the application
    When I remove the consignee off the application
    Then no consignee is set on the application
