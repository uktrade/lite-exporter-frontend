Feature: I want to be able to withdraw an active application

  @LT-995-Withdraw-active-application
    Scenario: Withdraw an active application
      Given I go to exporter homepage and choose Test Org
      And I create a standard application via api
      When I click on applications
      And I click on application previously created
      When I click the button 'Withdraw Application'
      Then I should see a confirmation page
      And I select the yes radiobutton
      And I click submit
      Then the application will have the status "Withdrawn"
      And I won't be able to see the withdraw button
