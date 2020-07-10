@exporter @all
Feature: I want to register an organisation
  As an exporter-to-be
  I want to register an organisation
  So that I can export my products in the future

  @LT_1024_register_an_organisation @regression
  Scenario: Register a commercial organisation
    Given I am not logged in
    And I register but I don't belong to an organisation
    When I sign as user without an organisation registered
    And I register a new commercial organisation
    Then I should see a success page


  @LT_1024_register_an_individual_organisation @regression
  Scenario: Register a individual organisation
    Given I am not logged in
    And I register but I don't belong to an organisation
    When I sign as user without an organisation registered
    And I register a new individual organisation
    Then I should see a success page

  Scenario: Signing in with no organisation registered should take us to create account page
    Given I register but I don't belong to an organisation
    When I sign as user without an organisation registered
    Then I should see create account page

  Scenario: Accessing applications without registering an organisation
    Given I register but I don't belong to an organisation
    And I sign as user without an organisation registered
    When I access my applications
    Then I should see create account page
