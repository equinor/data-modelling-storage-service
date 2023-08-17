# Changelog

## [1.3.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.2.3...v1.3.0) (2023-08-17)


### Features

* add validate existing entity endpoint ([369f29c](https://github.com/equinor/data-modelling-storage-service/commit/369f29c91792c60159e49a17f6d30f807860a4ad))


### Bug Fixes

* add type attribute to ViewConfig blueprint ([037c4ba](https://github.com/equinor/data-modelling-storage-service/commit/037c4ba943452cd52691fde9e7d5145e0352e9e9))
* bug with adding optional attribute with document add endpoint ([af0a764](https://github.com/equinor/data-modelling-storage-service/commit/af0a7643be670d017c4dca6e92544935290c737e))
* correct call to create_default_array() from _get_entity() ([35332dd](https://github.com/equinor/data-modelling-storage-service/commit/35332dd87e2648f76384bb3275d344b090b8c5ac))
* improve error message from resolve_reference ([1039f0d](https://github.com/equinor/data-modelling-storage-service/commit/1039f0d1f480187b4bb8f43ada6945cf36964b17))
* modeling error in instantiate_entity.feature ([e42508d](https://github.com/equinor/data-modelling-storage-service/commit/e42508db1f3ced145cd0535978668dbc72ae58de))
* modeling issue ([f9baf61](https://github.com/equinor/data-modelling-storage-service/commit/f9baf61fbb884184f2c33542bb1beb4a5484ad3a))
* move validation of entity of type object from _validate_list to  _validate_complex_attribute ([5d443f3](https://github.com/equinor/data-modelling-storage-service/commit/5d443f3e06fff18a600ebc2be1fbd9e46bf784e0))
* package content should be storage non-contained ([23be8ac](https://github.com/equinor/data-modelling-storage-service/commit/23be8aca9367e5079df67d595377c69a4e9f5582))
* remove insert_reference endpoint and use document add instead ([811b1c6](https://github.com/equinor/data-modelling-storage-service/commit/811b1c670bfbccf4aec588ac82276739c4e96247))
* remove name attribute from Node class ([8ab9721](https://github.com/equinor/data-modelling-storage-service/commit/8ab97214593d6ca0044eb6d6ebdbabd208c59087))
* remove outdated call to create_default_array_recursive() ([6628247](https://github.com/equinor/data-modelling-storage-service/commit/6628247b511c21b62dcc0752f29dc1774694976e))
* simplify logic inside create_default_array() ([9de7d4c](https://github.com/equinor/data-modelling-storage-service/commit/9de7d4cf3e7505dfdf8050f51b5186598acde7d5))
* update split functionality in document service's add() ([fa9588a](https://github.com/equinor/data-modelling-storage-service/commit/fa9588a19db1265657199f0b177ce9279c5a2d99))


### Documentation

* create docstring for create_default_array() ([623a1b4](https://github.com/equinor/data-modelling-storage-service/commit/623a1b4bef86161f18142253118d86b8ab530374))


### Miscellaneous Chores

* fix links in validate tests ([ac36a9c](https://github.com/equinor/data-modelling-storage-service/commit/ac36a9c415f7b0d5c764555d4a3442a40d5f9425))
* formatting ([0ecdfc0](https://github.com/equinor/data-modelling-storage-service/commit/0ecdfc066025fc847ba1accd6ebada60f2a6f79e))
* update codeowners ([5d62311](https://github.com/equinor/data-modelling-storage-service/commit/5d62311407a0de850f8e859f1ed33d2f074a7e48))
* update Dimension class docstring ([a0591b2](https://github.com/equinor/data-modelling-storage-service/commit/a0591b2abf98da5b82a5eb6dad21452ee8b97f5c))
* update instantiate endpoint docstring ([ad080c6](https://github.com/equinor/data-modelling-storage-service/commit/ad080c689e4df4789c2889c1da67cc4ca2d454c9))
* upgrade packages ([5061b06](https://github.com/equinor/data-modelling-storage-service/commit/5061b06134e6073d92472b129b5618ae347da176))


### Code Refactoring

* create_default_array ([f6cd4e7](https://github.com/equinor/data-modelling-storage-service/commit/f6cd4e7574ff9a2f626cbe6c43cbd178a7a40a48))
* move docstring from _get_entity() to CreateEntity class ([336411c](https://github.com/equinor/data-modelling-storage-service/commit/336411cc1de7cdd06949a650b346235c369285b1))
* rename files to be equal to their use_case_functions ([256849d](https://github.com/equinor/data-modelling-storage-service/commit/256849d6bc3973476084d831d68019ac2430a434))
* rename resolve_document to resolve_references_in_entity ([1b3199b](https://github.com/equinor/data-modelling-storage-service/commit/1b3199bf6b1668ee4da0ef191753191b5f72c22a))
* rename resolve_reference.py to resolve_address.py ([18ed96d](https://github.com/equinor/data-modelling-storage-service/commit/18ed96d3a5394a9c8f978f196747ef92ad48e8bf))
* rename resolve_reference() from resolve_reference.py to resolve_address ([a7be4d5](https://github.com/equinor/data-modelling-storage-service/commit/a7be4d573c9e319699bab2267e2c2f9c858a8e16))
* rename ResolvedReference to ResolvedAddress ([ea6d07c](https://github.com/equinor/data-modelling-storage-service/commit/ea6d07c302218dc3b70067db6af06bf6b1e439d8))
* use blueprint's default value in create_default_array instead of blueprint_attribute ([658e42f](https://github.com/equinor/data-modelling-storage-service/commit/658e42f1386a7e53b42c3e0944718161b28c2d6a))
* use depth to control resolving references ([83ccd1b](https://github.com/equinor/data-modelling-storage-service/commit/83ccd1b8256793206495d74ebee9fe3f9d86de43))


### Tests

* add behave test for validate endpoints ([305b1bb](https://github.com/equinor/data-modelling-storage-service/commit/305b1bba490f22604f0e009b1c56beb11977da0c))
* fix modeling errors in test_tree_dict_conversion.py ([f529465](https://github.com/equinor/data-modelling-storage-service/commit/f52946533bfa001bd8ea4334e07ce02378b67f72))
* update formatting and fix modeling error in validation bdd tests ([f0d463d](https://github.com/equinor/data-modelling-storage-service/commit/f0d463d5ad34e4c013a726d685837c9074819289))
