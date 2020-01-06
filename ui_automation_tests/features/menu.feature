@exporter @all
Feature: Go to each item from the homepage

  @verify_build
  Scenario: Go to each item from the homepage
    Given I go to exporter homepage and choose Test Org
    When I refresh the page
    Then Log out link is displayed
    When I click on applications
    Then Log out link is displayed
    When I go to exporter homepage
    And I click on goods link
    Then Log out link is displayed
    When I go to exporter homepage
    And I click on end user advisories
    Then Log out link is displayed
    When I go to exporter homepage
    And I click on the manage my organisation link
    Then Log out link is displayed
