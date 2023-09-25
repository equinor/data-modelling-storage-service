# Changelog

## [1.5.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.4.0...v1.5.0) (2023-09-25)


### Features

* populate data source at startup using environment variable ([ed5534f](https://github.com/equinor/data-modelling-storage-service/commit/ed5534f973073c107162d14af962296b5d00ae53))
* support app registration with a Federated Credential to login ([7e1f7c7](https://github.com/equinor/data-modelling-storage-service/commit/7e1f7c72dee1b1d80c0b02db0fe75ddbd31a8c9a))
* validate blueprint attribute default ([e1e69a7](https://github.com/equinor/data-modelling-storage-service/commit/e1e69a75285c08ca135ccde298658c5d4e4ed2fa))


### Tests

* made get_mock_document_service only used in setUps ([41b9b25](https://github.com/equinor/data-modelling-storage-service/commit/41b9b256a87e03c1d025a5999b0d0ff67df110bb))
* made simos blueprints explicit ([e5d3335](https://github.com/equinor/data-modelling-storage-service/commit/e5d3335c65290dd2ca12e9e4957fd7c7e4d9ea40))
* make it explicit ([b940e6c](https://github.com/equinor/data-modelling-storage-service/commit/b940e6cb4aa70e05497c9b71e18d344d00be53d8))
* move into folders ([145932a](https://github.com/equinor/data-modelling-storage-service/commit/145932aa6b5b307c1a376dfe425e087f0b14c2aa))
* moved a test into correct folder ([7c5a5a4](https://github.com/equinor/data-modelling-storage-service/commit/7c5a5a4a83c00395ca5297fe4cf299369aa50bb0))
* moved a test utils into the test_uitls folder ([ec60a2a](https://github.com/equinor/data-modelling-storage-service/commit/ec60a2ac176340a1446e53c528e7696c90f032b0))
* moving tests into neat folders ([9996fdd](https://github.com/equinor/data-modelling-storage-service/commit/9996fdd36d7edcef8a35b9596000acd14b13e448))
* require a list of blueprints, to make the mocker data-less ([aab7af0](https://github.com/equinor/data-modelling-storage-service/commit/aab7af08c03e49f7c85b536c260cfc4a2f063338))
* revert one little change ([5a8e2df](https://github.com/equinor/data-modelling-storage-service/commit/5a8e2df221a4fc39d8afc109f754b4ec143e4722))
* split up two tests into two classes ([f1dc67e](https://github.com/equinor/data-modelling-storage-service/commit/f1dc67e8d7443e6ec02a116dd4f46672846a03de))

## [1.4.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.3.1...v1.4.0) (2023-09-15)


### Features

* error handling in has-key-value-pair ([ea77488](https://github.com/equinor/data-modelling-storage-service/commit/ea7748850d9ea11b5e76a69af884981c8dafcf21))
* extend testing coverage of scrypt method to be complete ([a9c8739](https://github.com/equinor/data-modelling-storage-service/commit/a9c873935f1185c985cef285f9a769d74d19613e))


### Code Refactoring

* add oauth scope to swagger ([3a5a30a](https://github.com/equinor/data-modelling-storage-service/commit/3a5a30a7dc0a3d56d46319ec6ce08aa96f387c1c))
* remove unused attribute node.error_message ([ea7fc43](https://github.com/equinor/data-modelling-storage-service/commit/ea7fc43806bcc301452ff1dbc3791fa793b6622d))
* remove unused test for attribute Node.error_message ([0207d6f](https://github.com/equinor/data-modelling-storage-service/commit/0207d6f979c5f5110beafb2eea83341fe1174af1))
* removed unused method ([48ff4f2](https://github.com/equinor/data-modelling-storage-service/commit/48ff4f25ac5ff0509e1e9cd901bb21badf05fdda))
* Removed unused methods and their tests ([8c1b6f8](https://github.com/equinor/data-modelling-storage-service/commit/8c1b6f8600dbc708a2431489065044b252c8fa80))
* renamed or moved files ([6f1a07b](https://github.com/equinor/data-modelling-storage-service/commit/6f1a07ba1a9ab094476cd46d1a058d66f944517a))
* split up mocking in the unit tests ([08d7374](https://github.com/equinor/data-modelling-storage-service/commit/08d7374e8efe980157e2503154cc26205c9b79bc))


### Tests

* added test cases so that the hashing is secure ([c9e9af8](https://github.com/equinor/data-modelling-storage-service/commit/c9e9af88ce67ece86904c17f4cc23649f88dd371))
* be explicit about which SIMOS blueprints are allowed in test-data ([cb2c37c](https://github.com/equinor/data-modelling-storage-service/commit/cb2c37c26419e2eaaa291fdacb2400e0a485691b))
* clean up mock blueprint provider, and also simpler blueprintNames ([50a8954](https://github.com/equinor/data-modelling-storage-service/commit/50a8954d9157e1e597d9079d1d5ad02377dfd86c))
* import mock_document_service directly ([88dcf63](https://github.com/equinor/data-modelling-storage-service/commit/88dcf63cfd13c965aa9f4a6608e3cc590aea1eed))
* moved check_existance into feauture folder ([e9a5410](https://github.com/equinor/data-modelling-storage-service/commit/e9a5410322d60e42ed369578375bb4f0dc19ecb2))
* moved into more nested folder ([40f4ec1](https://github.com/equinor/data-modelling-storage-service/commit/40f4ec1907872568ab92c657f5b7b3fa9dd14821))
* refactored get_blueprint to be less hard-coded ([06e9cbd](https://github.com/equinor/data-modelling-storage-service/commit/06e9cbdf29c3736e6d915639ebfde583ba42c564))
* remove unused parameters in testing file ([b83eb6f](https://github.com/equinor/data-modelling-storage-service/commit/b83eb6f31ca2c8edbcd5395aa08da72b533d475b))
* remove unused recipes in testing blueprint ([d18037e](https://github.com/equinor/data-modelling-storage-service/commit/d18037ef898439ea404f637bde5225032250b9ae))
* remove unused recipes in testing blueprint ([79ef90e](https://github.com/equinor/data-modelling-storage-service/commit/79ef90e36e249cdce3d18cf6ba6dbc31929e65f3))
* remove unused recipes in testing blueprint ([18eeeb9](https://github.com/equinor/data-modelling-storage-service/commit/18eeeb9e522dc9b91866a8df17e42e20bcf6a33d))
* renamed blueprint_4 to Blueprint4 ([4fc2742](https://github.com/equinor/data-modelling-storage-service/commit/4fc274226a20f5b46aac2a8e8314a32d55a8685f))
* renamed recursive_blueprint to Recursive ([6cb4686](https://github.com/equinor/data-modelling-storage-service/commit/6cb4686b837523a0f1e84098c1ffb767a98ad817))
* split up test file into two separate files ([3085947](https://github.com/equinor/data-modelling-storage-service/commit/3085947f1bce0509a30c98980829baf18706785e))
* tree tests refactor ([0785b9d](https://github.com/equinor/data-modelling-storage-service/commit/0785b9d6042a966b5e81a821a44505284478f925))

## [1.3.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.3.0...v1.3.1) (2023-09-01)


### Bug Fixes

* add job to case ([eec8ee4](https://github.com/equinor/data-modelling-storage-service/commit/eec8ee4a565fe3ac48152eb2ae3d1d4020fc5b87))


### Code Refactoring

* use method to find attribute ([8ea896d](https://github.com/equinor/data-modelling-storage-service/commit/8ea896d12c259fc6ff2a8704f8f957bbc8a8d161))

## [1.3.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.2.3...v1.3.0) (2023-08-29)


### Features

* add validate existing entity endpoint ([369f29c](https://github.com/equinor/data-modelling-storage-service/commit/369f29c91792c60159e49a17f6d30f807860a4ad))
* endpoint for checking if document exist ([9ab8e0f](https://github.com/equinor/data-modelling-storage-service/commit/9ab8e0f653a3f745a93709ed94b450fcec58b677))


### Bug Fixes

* add type attribute to ViewConfig blueprint ([037c4ba](https://github.com/equinor/data-modelling-storage-service/commit/037c4ba943452cd52691fde9e7d5145e0352e9e9))
* also changed test to reflect new error message ([58fcf99](https://github.com/equinor/data-modelling-storage-service/commit/58fcf997ec91a6363fbaab7292617b33ebd24759))
* bug with adding optional attribute with document add endpoint ([af0a764](https://github.com/equinor/data-modelling-storage-service/commit/af0a7643be670d017c4dca6e92544935290c737e))
* bug with updating a list from update document endpoint ([788508a](https://github.com/equinor/data-modelling-storage-service/commit/788508a6e1c988fd9499e57aeb17af647efc752c))
* content in File blueprint should not be model uncontained ([2ac98d1](https://github.com/equinor/data-modelling-storage-service/commit/2ac98d16b21b83b6bc61eaae7dd84e7c509e1d86))
* correct call to create_default_array() from _get_entity() ([35332dd](https://github.com/equinor/data-modelling-storage-service/commit/35332dd87e2648f76384bb3275d344b090b8c5ac))
* delete blobs corretly ([801a73b](https://github.com/equinor/data-modelling-storage-service/commit/801a73b742095b1312dcbfa878a3980fc3d0d25f))
* **documentAdd:** lower depth ([8dd50c2](https://github.com/equinor/data-modelling-storage-service/commit/8dd50c2c632a9a550434b273d3962358f446af26))
* exception prints all invalid data sources ([d49a853](https://github.com/equinor/data-modelling-storage-service/commit/d49a8534204c2722a315c5a62aa7129af22e4950))
* fileresponse cannot be used as a response model ([7d8dedc](https://github.com/equinor/data-modelling-storage-service/commit/7d8dedc8462ce5fef6b9674471ff9c44d389dfee))
* fixed unit test cases after required attributes no longer can be deleted ([05428d2](https://github.com/equinor/data-modelling-storage-service/commit/05428d2ea25fd648020f3c39a871efc49e32c55e))
* improve error message from resolve_reference ([1039f0d](https://github.com/equinor/data-modelling-storage-service/commit/1039f0d1f480187b4bb8f43ada6945cf36964b17))
* modeling error in instantiate_entity.feature ([e42508d](https://github.com/equinor/data-modelling-storage-service/commit/e42508db1f3ced145cd0535978668dbc72ae58de))
* modeling issue ([f9baf61](https://github.com/equinor/data-modelling-storage-service/commit/f9baf61fbb884184f2c33542bb1beb4a5484ad3a))
* move validation of entity of type object from _validate_list to  _validate_complex_attribute ([5d443f3](https://github.com/equinor/data-modelling-storage-service/commit/5d443f3e06fff18a600ebc2be1fbd9e46bf784e0))
* package content should be storage non-contained ([23be8ac](https://github.com/equinor/data-modelling-storage-service/commit/23be8aca9367e5079df67d595377c69a4e9f5582))
* remove insert_reference endpoint and use document add instead ([811b1c6](https://github.com/equinor/data-modelling-storage-service/commit/811b1c670bfbccf4aec588ac82276739c4e96247))
* remove name attribute from Node class ([8ab9721](https://github.com/equinor/data-modelling-storage-service/commit/8ab97214593d6ca0044eb6d6ebdbabd208c59087))
* remove outdated call to create_default_array_recursive() ([6628247](https://github.com/equinor/data-modelling-storage-service/commit/6628247b511c21b62dcc0752f29dc1774694976e))
* remove reference feature from the API ([3fce6d5](https://github.com/equinor/data-modelling-storage-service/commit/3fce6d5d3754bd519c04a645f37f6f433bf9587a))
* set timeout ([d04244a](https://github.com/equinor/data-modelling-storage-service/commit/d04244a68533e47a3a598698a6685696616869e3))
* setting node uid correctly ([8b5afc7](https://github.com/equinor/data-modelling-storage-service/commit/8b5afc7f6fd7418ef611b8a5286a8ac0a1f530b2))
* simplify default storage recipe ([477203a](https://github.com/equinor/data-modelling-storage-service/commit/477203a55cfaf5dbdd055eb28031565ff803adfe))
* simplify logic inside create_default_array() ([9de7d4c](https://github.com/equinor/data-modelling-storage-service/commit/9de7d4cf3e7505dfdf8050f51b5186598acde7d5))
* update split functionality in document service's add() ([fa9588a](https://github.com/equinor/data-modelling-storage-service/commit/fa9588a19db1265657199f0b177ce9279c5a2d99))
* upgrade pre-commit version to allow new command ([c73abf5](https://github.com/equinor/data-modelling-storage-service/commit/c73abf5fe83a7079efb6860671dd4600d3efa9da))


### Documentation

* Adding docstrings ([d63fba6](https://github.com/equinor/data-modelling-storage-service/commit/d63fba6076dbd22e744eb30899f4fb35d69ef680))
* adding user as parameter in docstrings ([bb48747](https://github.com/equinor/data-modelling-storage-service/commit/bb48747872787c8383dbc74285e6e7d84509a8da))
* changed meta docstring to reflect the meta information about a blob ([b93b5c6](https://github.com/equinor/data-modelling-storage-service/commit/b93b5c63f3050e8d45c84bea19e41fc761119151))
* create docstring for create_default_array() ([623a1b4](https://github.com/equinor/data-modelling-storage-service/commit/623a1b4bef86161f18142253118d86b8ab530374))
* docstring for file_feature ([3151e80](https://github.com/equinor/data-modelling-storage-service/commit/3151e801810cf6a452ac1fe4da72acd85bc13e6c))
* docstring for meta_feature ([a3a069c](https://github.com/equinor/data-modelling-storage-service/commit/a3a069c5293cbbe07ec00340266d8faa194e4411))
* docstring for the health check endpoint ([6fb5971](https://github.com/equinor/data-modelling-storage-service/commit/6fb597197bc17b8c21229daca428c9069114a924))
* docstrings for ACL ([8a81a6e](https://github.com/equinor/data-modelling-storage-service/commit/8a81a6e19a2addc5af51f7f9191e33d6e9632c5c))
* docstrings for attribute_feature.py ([219748f](https://github.com/equinor/data-modelling-storage-service/commit/219748f127698fd9d31d726ba76e31117380db5c))
* docstrings for blob_feature.py ([b03fdad](https://github.com/equinor/data-modelling-storage-service/commit/b03fdadea80536446265a705854655b57ff69b52))
* docstrings for blueprint_feature.py ([0deded0](https://github.com/equinor/data-modelling-storage-service/commit/0deded05ac1a6230aceb0d1e9d6e2b0bc062bc3d))
* docstrings for datasource_feature.py ([1d1b6dd](https://github.com/equinor/data-modelling-storage-service/commit/1d1b6ddeba58accd652697a0c1fb6ccbcc44ee6e))
* docstrings for document_feature.py ([950603b](https://github.com/equinor/data-modelling-storage-service/commit/950603b32b84deca8edbc02b86207f01345cf823))
* docstrings for endpoints ([0d0c7c3](https://github.com/equinor/data-modelling-storage-service/commit/0d0c7c30b7d69e438405df81db2bb1385b910234))
* docstrings for entity_feature.py.py ([cb69061](https://github.com/equinor/data-modelling-storage-service/commit/cb6906107d0eb315b97f68b60c5f60a2af8a98c3))
* docstrings for health check and lookup table ([2c6a77c](https://github.com/equinor/data-modelling-storage-service/commit/2c6a77c386be4e70ee33f148cb8c258df87ad35d))
* Editing docstrings according to KKJS comment ([2702a0b](https://github.com/equinor/data-modelling-storage-service/commit/2702a0be7b7a8010a0dec047bf5c56e0406a0bc5))
* minor fix, adding a '-' to a docstring ([4974c7e](https://github.com/equinor/data-modelling-storage-service/commit/4974c7e960e284de5588f16758079a3d1f546131))
* minor fix, removed something from acl docstring ([5616018](https://github.com/equinor/data-modelling-storage-service/commit/5616018fe9699bb00be6568eff964f1d49f8029d))
* newline remove ([aae4768](https://github.com/equinor/data-modelling-storage-service/commit/aae47688a8ee6c395225408f905ae82503c6798e))
* ran pre-commit ([e180b31](https://github.com/equinor/data-modelling-storage-service/commit/e180b3136c4ec14d0156f3065ca7837ffd31b858))
* simplified readme steps into something that works ([fa689f4](https://github.com/equinor/data-modelling-storage-service/commit/fa689f4785563ae2ee9e0a03bde45511aba135a3))
* update pre commit docs ([903b682](https://github.com/equinor/data-modelling-storage-service/commit/903b6829d9195a6328929eb0327d3f7c87352fc8))
* update reset command in readme ([2347ec9](https://github.com/equinor/data-modelling-storage-service/commit/2347ec941bb245561728f086844cbaa058d11990))


### Styles

* fix flake8 errors ([5dbdaf0](https://github.com/equinor/data-modelling-storage-service/commit/5dbdaf0c4b2dcb89ec08995f290c8a60c582519e))
* run pretty-format-json ([ab83819](https://github.com/equinor/data-modelling-storage-service/commit/ab8381995ce0a3a041b06e1090924e2e231aafef))


### Miscellaneous Chores

* add version to app and pyproject ([7f49729](https://github.com/equinor/data-modelling-storage-service/commit/7f49729b1777f13d4717b3b30899308efec2f00d))
* fix links in validate tests ([ac36a9c](https://github.com/equinor/data-modelling-storage-service/commit/ac36a9c415f7b0d5c764555d4a3442a40d5f9425))
* formatting ([0ecdfc0](https://github.com/equinor/data-modelling-storage-service/commit/0ecdfc066025fc847ba1accd6ebada60f2a6f79e))
* update codeowners ([5d62311](https://github.com/equinor/data-modelling-storage-service/commit/5d62311407a0de850f8e859f1ed33d2f074a7e48))
* update Dimension class docstring ([a0591b2](https://github.com/equinor/data-modelling-storage-service/commit/a0591b2abf98da5b82a5eb6dad21452ee8b97f5c))
* update instantiate endpoint docstring ([ad080c6](https://github.com/equinor/data-modelling-storage-service/commit/ad080c689e4df4789c2889c1da67cc4ca2d454c9))
* update pre-commits ([539de6e](https://github.com/equinor/data-modelling-storage-service/commit/539de6ee6bbc37c5958230df9f220bf8aea24a32)), closes [#507](https://github.com/equinor/data-modelling-storage-service/issues/507)
* upgrade packages ([5061b06](https://github.com/equinor/data-modelling-storage-service/commit/5061b06134e6073d92472b129b5618ae347da176))


### Code Refactoring

* add method to data source to get storage affinity ([53e2911](https://github.com/equinor/data-modelling-storage-service/commit/53e29112c978455e6312998e93fc2b9b36653265))
* Added type hinting ([9e01b3e](https://github.com/equinor/data-modelling-storage-service/commit/9e01b3e8af51c53d56b5d77a21b1c8d3717f4765))
* Black reformat ([700acea](https://github.com/equinor/data-modelling-storage-service/commit/700acea3cecf7d5d7d08bf85bff6811a869b3b7d))
* create_default_array ([f6cd4e7](https://github.com/equinor/data-modelling-storage-service/commit/f6cd4e7574ff9a2f626cbe6c43cbd178a7a40a48))
* isort sorting ([06af5db](https://github.com/equinor/data-modelling-storage-service/commit/06af5db73b03bf469309516724eabc552d43889c))
* move add document logic to use case instead of document service ([f4cc6a8](https://github.com/equinor/data-modelling-storage-service/commit/f4cc6a85c21684977d40c05c6072c64bb5f2f0a5))
* move docstring from _get_entity() to CreateEntity class ([336411c](https://github.com/equinor/data-modelling-storage-service/commit/336411cc1de7cdd06949a650b346235c369285b1))
* move get acl from document service to use case ([a7828b9](https://github.com/equinor/data-modelling-storage-service/commit/a7828b987c7c2608cbc9eb3ca7d1346f875ff5d9))
* move set acl from document service to use case ([ff58ee5](https://github.com/equinor/data-modelling-storage-service/commit/ff58ee5b367de0fb0c9dfd73e06eac369cdf1211))
* move update document logic to use case instead of document service ([ea6344b](https://github.com/equinor/data-modelling-storage-service/commit/ea6344b5138385df2f16f12f5acf317df2cbb330))
* refactored search-use-case in order to make it more readable ([9ab50c3](https://github.com/equinor/data-modelling-storage-service/commit/9ab50c38b2680eccae19e80883307e22e630d692))
* removed reference to private method, and changed method to be more understandable ([e7e6d89](https://github.com/equinor/data-modelling-storage-service/commit/e7e6d89741d8384d124c760a0f61cbdb3e72cb26))
* rename files to be equal to their use_case_functions ([256849d](https://github.com/equinor/data-modelling-storage-service/commit/256849d6bc3973476084d831d68019ac2430a434))
* rename resolve_document to resolve_references_in_entity ([1b3199b](https://github.com/equinor/data-modelling-storage-service/commit/1b3199bf6b1668ee4da0ef191753191b5f72c22a))
* rename resolve_reference.py to resolve_address.py ([18ed96d](https://github.com/equinor/data-modelling-storage-service/commit/18ed96d3a5394a9c8f978f196747ef92ad48e8bf))
* rename resolve_reference() from resolve_reference.py to resolve_address ([a7be4d5](https://github.com/equinor/data-modelling-storage-service/commit/a7be4d573c9e319699bab2267e2c2f9c858a8e16))
* rename ResolvedReference to ResolvedAddress ([ea6d07c](https://github.com/equinor/data-modelling-storage-service/commit/ea6d07c302218dc3b70067db6af06bf6b1e439d8))
* Rename string classes to convention ([ce7c10e](https://github.com/equinor/data-modelling-storage-service/commit/ce7c10e534f11f86fb30806b7eb5cf24f3260e41))
* renaming to be more clear ([802c16b](https://github.com/equinor/data-modelling-storage-service/commit/802c16bda8e166b8f72eaa108cdbeddb22999649))
* use blueprint's default value in create_default_array instead of blueprint_attribute ([658e42f](https://github.com/equinor/data-modelling-storage-service/commit/658e42f1386a7e53b42c3e0944718161b28c2d6a))
* use depth to control resolving references ([83ccd1b](https://github.com/equinor/data-modelling-storage-service/commit/83ccd1b8256793206495d74ebee9fe3f9d86de43))
* using getter ([eed6c54](https://github.com/equinor/data-modelling-storage-service/commit/eed6c542179e62ae6f3039887e802bb6c74e9d48))


### Tests

* add behave test for validate endpoints ([305b1bb](https://github.com/equinor/data-modelling-storage-service/commit/305b1bba490f22604f0e009b1c56beb11977da0c))
* add testing of reference update ([cfc308c](https://github.com/equinor/data-modelling-storage-service/commit/cfc308cd857b968022a53ee13409893305bb34de))
* fix modeling errors in test_tree_dict_conversion.py ([f529465](https://github.com/equinor/data-modelling-storage-service/commit/f52946533bfa001bd8ea4334e07ce02378b67f72))
* update formatting and fix modeling error in validation bdd tests ([f0d463d](https://github.com/equinor/data-modelling-storage-service/commit/f0d463d5ad34e4c013a726d685837c9074819289))


### Continuous Integration

* avoid running no-commit-to-branch on PR merge ([4dfbf25](https://github.com/equinor/data-modelling-storage-service/commit/4dfbf259334c28c2d9e7a9cd201df0733d04d5be))
* **release:** add release please job ([9bfeae6](https://github.com/equinor/data-modelling-storage-service/commit/9bfeae64ad8fdd43182eaeaa248c28230b03b306))
