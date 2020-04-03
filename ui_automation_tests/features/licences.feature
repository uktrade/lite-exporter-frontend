@licences @all
Feature: I want to be able to view licences as an exporter user

  @LT_1254_view_licences @regression
  Scenario: View my standard application licences
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    And I create a licence for my application
    When I go to the licences page
    Then I see my standard licence
