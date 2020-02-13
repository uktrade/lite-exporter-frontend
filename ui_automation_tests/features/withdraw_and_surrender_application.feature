@all @status
Feature: I want to be able to withdraw an active application

  @LT_995_Withdraw_active_application @regression
    Scenario: Withdraw an active application
      Given I go to exporter homepage and choose Test Org
      And I create a standard application via api
      When I go to application previously created
      And I click the button 'Withdraw Application'
      Then I should see a confirmation page
      When I select the yes radiobutton
      And I click submit
      Then the application will have the status "Withdrawn"
      And I won't be able to see the withdraw button
      And the edit application button is not present
      When I click the notes tab
      Then the case note text area is not present

  @LT_979_surrender_finalised_application @regression
    Scenario: Surrender a finalised application
      Given I go to exporter homepage and choose Test Org
      And I create a standard application via api
      And The application has been approved
      When I go to application previously created
      And I click the button 'Surrender Application'
      Then I should see a confirmation page
      When I select the yes radiobutton
      And I click submit
      Then the application will have the status "Surrendered"
      And I won't be able to see the surrender button
      And the edit application button is not present
      When I click the notes tab
      Then the case note text area is not present