@exporter @licence @all @submit
Feature: Licence
  As a...

  Scenario: Apply for a licence to draft
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    Then I see the application overview

  Scenario: Delete application from draft
    Given I go to exporter homepage
    When I click drafts
    When I click the application
    When I delete the application

  Scenario: Submit application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click sites link
    When I select the site at position
 #   When I submit the application
#    Then application is submitted

  Scenario: Error message when there is no site selected
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click continue
    Then I see no sites attached error message

