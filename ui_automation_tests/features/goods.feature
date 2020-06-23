@goods @all
Feature: I want to edit and remove goods on the goods list
  As a logged in exporter
  I want to add edit and remove goods on my goods list
  So that I can ensure the correct goods are listed on my goods list

  @LT_928_edit @regression
  Scenario: Add, edit and delete good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "one" for a good
    And I add a good with description "123 pistol" part number "321" controlled "Yes" control code "ML1a" and graded "yes"
    And I add the goods grading with prefix "abc" grading "nato_restricted" suffix "def" issuing authority "NATO" reference "12345" Date of issue "10-05-2015"
    And I specify the good details military use "yes_modified" component "yes_general" and information security "Yes"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I get the goods ID
    Then I see good in goods list
    When I edit the good to description "edited" part number "321" controlled "Yes" and control list entry "ML1a"
    And I edit the good details to military use "yes_designed" component "yes_designed" information security "No"
    Then I see my edited good details in the good page
    When I delete my good
    Then my good is no longer in the goods list

  @LT_1006_add_clc_query_good @regression
  Scenario: Add queried good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "one" for a good
    And I add a good with description "Hand pistol" part number "321" controlled "Unsure" control code " " and graded "grading_required"
    And I specify the good details military use "yes_designed" component "yes_modified" and information security "No"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I raise a clc query control code "ML1a" clc description "I believe it is ML1a" and pv grading reason "I believe the good requires grading"
    Then I see good information
    And I see the good is in a query

  @LT_1262_add_good_without_document @regression
  Scenario: Add a new good without a document for a valid reason
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "one" for a good
    And I add a good with description "Hand pistol" part number "321" controlled "Unsure" control code " " and graded "no"
    And I specify the good details military use "no" component "no" and information security "No"
    And I select that I cannot attach a document
    Then I see ECJU helpline details
    When I select a valid missing document reason
    When I click the back link
    Then My good is created

  @LT_2704_add_software_good_and_edit @regression
  Scenario: Add, edit and delete good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "three-software" for a good
    And I add a good with description "123 pistol" part number "321" controlled "Yes" control code "ML1a" and graded "yes"
    And I add the goods grading with prefix "abc" grading "nato_restricted" suffix "def" issuing authority "NATO" reference "12345" Date of issue "10-05-2015"
    And I specify software and technology purpose details for a good that is in those categories
    And I specify the good details military use "yes_modified" component "yes_general" and information security "Yes"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I get the goods ID
    Then I see good in goods list
    When I edit the good to description "edited" part number "321" controlled "Yes" and control list entry "ML1a"
    And I edit the good details to military use "yes_designed" component "yes_designed" information security "No"
    And I edit the software and technology purpose details for a good to "edited software purpose"
    Then I see my edited good details in the good page
    When I delete my good
    Then my good is no longer in the goods list
