@exporter @all
Feature: Go to each item from the homepage

  @verify_build
  Scenario: Go to each item from the homepage
    Given I go to exporter homepage and choose Test Org
    When I refresh the page
    Then The log out link is displayed
    When I click on applications
    Then The log out link is displayed
    When I go to exporter homepage
    And I click on goods link
    Then The log out link is displayed
    When I go to exporter homepage
    And I click on end user advisories
    Then The log out link is displayed
    When I go to exporter homepage
    And I click on the manage my organisation link
    Then The log out link is displayed
