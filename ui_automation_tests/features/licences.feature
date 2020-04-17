@licences @all
Feature: I want to be able to view licences as an exporter user

  @LT_1254_view_licences_standard @regression
  Scenario: View my standard application licences
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    And I create "approve" final advice
    And I create a licence for my application with "approve" decision document and good decisions
    When I go to the licences page
    Then I see my standard licence
    When I view my licence
    Then I see all the typical licence details
    And I see my standard application licence details

  @LT_1254_view_licences_open @regression
  Scenario: View my open application licences
    Given I go to exporter homepage and choose Test Org
    And I create an open application via api
    And I create "approve" final advice for open application
    And I create a licence for my application with "approve" decision document
    When I go to the licences page
    Then I see my open licence

  @LT_1254_view_licences_mod @regression
  Scenario: View my mod application licences
    Given I go to exporter homepage and choose Test Org
    And an Exhibition Clearance is created
    And I create "approve" final advice
    And I create a licence for my application with "approve" decision document
    When I go to the licences page
    And I click on the clearances tab
    Then I see my exhibition licence
