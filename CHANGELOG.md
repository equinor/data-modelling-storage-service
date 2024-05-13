# Changelog

## [1.26.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.25.3...v1.26.0) (2024-05-13)


### Features

* cache documents in redis ([09f520e](https://github.com/equinor/data-modelling-storage-service/commit/09f520ef6d557b37608eaf41a6e4a4e3ca31cf17))

## [1.25.3](https://github.com/equinor/data-modelling-storage-service/compare/v1.25.2...v1.25.3) (2024-05-06)


### Bug Fixes

* **mongo:** retry failed requests ([54f0bc1](https://github.com/equinor/data-modelling-storage-service/commit/54f0bc1a4aa504a8c957177878c7e84a9540825e))

## [1.25.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.25.1...v1.25.2) (2024-04-29)


### Bug Fixes

* create datasource should be replace existing ([0461b13](https://github.com/equinor/data-modelling-storage-service/commit/0461b13868a1ffbbca31201bb5ebc8e39b5f98d2))


### Performance Improvements

* cache documents in 'resolve_document' ([dc74f5c](https://github.com/equinor/data-modelling-storage-service/commit/dc74f5c79a6579839edb953708d57b7a929347ea))


### Build System

* **deps:** bump idna from 3.6 to 3.7 ([19cf419](https://github.com/equinor/data-modelling-storage-service/commit/19cf41961eece151c4c4d40dffb337fef1c89585))
* **deps:** bump pymongo from 4.6.1 to 4.6.3 ([0552b25](https://github.com/equinor/data-modelling-storage-service/commit/0552b2567498d20ae7d83f7a170d99de33512214))

## [1.25.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.25.0...v1.25.1) (2024-04-26)


### Performance Improvements

* keep fetched blueprints. Custom blueprint 'get_document' ([c47d71a](https://github.com/equinor/data-modelling-storage-service/commit/c47d71a60fcf0416b9890a422fb103ededa1eb14))
* move internal db to memory-DB ([07c1b71](https://github.com/equinor/data-modelling-storage-service/commit/07c1b7176573948bfe58cba75e43697a685b73f4))

## [1.25.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.24.0...v1.25.0) (2024-04-18)


### Features

* optional name and description to RecipeLink ([d46e871](https://github.com/equinor/data-modelling-storage-service/commit/d46e871fbe32fd476de8b78717f732dde4a36668))


### Performance Improvements

* **address_resolver:** return early when finding a filter match ([a4b91c2](https://github.com/equinor/data-modelling-storage-service/commit/a4b91c2d45a615cc55505c3d36bb398f6289fba3))
* cache on get_data_source ([58ac840](https://github.com/equinor/data-modelling-storage-service/commit/58ac84037538a3d8e4006b26c0471989f50d92cd))

## [1.24.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.23.4...v1.24.0) (2024-04-08)


### Features

* plugable repositories ([85ae3d2](https://github.com/equinor/data-modelling-storage-service/commit/85ae3d25bb610a7c726403d3536927e920ac0618))

## [1.23.4](https://github.com/equinor/data-modelling-storage-service/compare/v1.23.3...v1.23.4) (2024-03-22)


### Bug Fixes

* no longer use gunicorn to scale workers ([7d71cbf](https://github.com/equinor/data-modelling-storage-service/commit/7d71cbf8963e229b84639160aef5787cbb657e68))


### Documentation

* README to be up-to-date ([e4c015f](https://github.com/equinor/data-modelling-storage-service/commit/e4c015f37afbb7995bd80075d93475434496263f))

## [1.23.3](https://github.com/equinor/data-modelling-storage-service/compare/v1.23.2...v1.23.3) (2024-03-22)


### Bug Fixes

* increase gunicorn timeout to 180s ([86b96ce](https://github.com/equinor/data-modelling-storage-service/commit/86b96ce95b23a8ddf39f8abf13492095ae3e0f10))

## [1.23.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.23.1...v1.23.2) (2024-03-14)


### Bug Fixes

* more info on 'failed to resolve reference' ([6f95b0a](https://github.com/equinor/data-modelling-storage-service/commit/6f95b0a3f696338233cb6e6a143f534293a55af8))

## [1.23.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.23.0...v1.23.1) (2024-03-05)


### Bug Fixes

* partial update only worked with complex ([0943483](https://github.com/equinor/data-modelling-storage-service/commit/094348342e65d960d4afcc61f89eb1af5598754d))


### Miscellaneous Chores

* add compliant badge ([0ce36a9](https://github.com/equinor/data-modelling-storage-service/commit/0ce36a99e1500230423b64f46fe365a816273c89))

## [1.23.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.22.1...v1.23.0) (2024-03-01)


### Features

* add versionNote to Meta. Reduce BP provider logging ([77ce14b](https://github.com/equinor/data-modelling-storage-service/commit/77ce14b653a5189411c84299d27b0380ab11a049))
* addDocument() return full address to the new entity ([b8701c1](https://github.com/equinor/data-modelling-storage-service/commit/b8701c12a99cec2a6ff372af6b48935b8de20f1a))


### Build System

* **deps:** bump cryptography from 42.0.3 to 42.0.4 ([f7e4e7c](https://github.com/equinor/data-modelling-storage-service/commit/f7e4e7c989574e5406731e8bd200d2fbb971c061))

## [1.22.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.22.0...v1.22.1) (2024-02-23)


### Miscellaneous Chores

* upgrade to pydantic v2 ([2803551](https://github.com/equinor/data-modelling-storage-service/commit/28035510ee70ab107531f5dc5caafff1a54d938e))

## [1.22.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.21.0...v1.22.0) (2024-02-22)


### Features

* automatically keep profiles for requests that are over time limit ([48f5a0c](https://github.com/equinor/data-modelling-storage-service/commit/48f5a0c6f1180d35e726a389da1e1d425ed0713e))

## [1.21.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.20.2...v1.21.0) (2024-02-20)


### Features

* profile requests ([c5c340a](https://github.com/equinor/data-modelling-storage-service/commit/c5c340a7504f3b2a1b2890aed62c1f49e80a71d8))
* store profiles in Azure blob storage ([322c2ed](https://github.com/equinor/data-modelling-storage-service/commit/322c2ed00f836a3ef7a1871fd8a77323bd0534c9))


### Code Refactoring

* do not save non references recursively ([f143aa5](https://github.com/equinor/data-modelling-storage-service/commit/f143aa52e41d0a265544909ff2d6923f52773959))
* remove intial flag from save method ([460658d](https://github.com/equinor/data-modelling-storage-service/commit/460658d917eb49e268138ffdf2af94adc7da96b6))
* save should find parent for contained nodes ([3a2c9ea](https://github.com/equinor/data-modelling-storage-service/commit/3a2c9eaed33b40ffab4fe936bd303f59630c2858))

## [1.20.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.20.1...v1.20.2) (2024-02-20)


### Continuous Integration

* disable cors in CI ([8bee9da](https://github.com/equinor/data-modelling-storage-service/commit/8bee9da52f94aee5b31775dd84f1fa6484266434))

## [1.20.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.20.0...v1.20.1) (2024-02-19)


### Bug Fixes

* gunicorn times out on some slow requests ([49029e8](https://github.com/equinor/data-modelling-storage-service/commit/49029e8ee8cf48fc8a9c5aa538b0e7cf60daba35))

## [1.20.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.19.1...v1.20.0) (2024-02-16)


### Features

* option to enforce uid on all complex children ([46fb91a](https://github.com/equinor/data-modelling-storage-service/commit/46fb91a3d540761b8d936fb44dbe96598692a9fa))

## [1.19.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.19.0...v1.19.1) (2024-02-15)


### Miscellaneous Chores

* change to resolve document for better performance ([95a267f](https://github.com/equinor/data-modelling-storage-service/commit/95a267f1fb09046e7fd988cc3a7c51b5cd0ca379))

## [1.19.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.18.5...v1.19.0) (2024-02-14)


### Features

* add azure app insight ([9d7a77c](https://github.com/equinor/data-modelling-storage-service/commit/9d7a77ca4e3fe9cabebbbf3e0942679fb64e1df5))


### Build System

* **deps:** bump python-multipart from 0.0.5 to 0.0.7 ([099c680](https://github.com/equinor/data-modelling-storage-service/commit/099c68017ef11a462a68e66ba78d558ffa5a569e))

## [1.18.5](https://github.com/equinor/data-modelling-storage-service/compare/v1.18.4...v1.18.5) (2024-02-08)


### Bug Fixes

* instantiate one blueprint provider only ([be6e128](https://github.com/equinor/data-modelling-storage-service/commit/be6e128183155771e59795f70c724a6e655f079f))
* remove debug ([a152691](https://github.com/equinor/data-modelling-storage-service/commit/a152691a42ca2e5337a8f332880cd0cf5415c21f))
* tests ([ec7cfbb](https://github.com/equinor/data-modelling-storage-service/commit/ec7cfbb78c8db9f78a2033ca657f96cf1e528f1f))
* trying singleton blueprint_provider ([11f4bf9](https://github.com/equinor/data-modelling-storage-service/commit/11f4bf94734a2725134573fe704d100bf7e079f1))

## [1.18.4](https://github.com/equinor/data-modelling-storage-service/compare/v1.18.3...v1.18.4) (2024-02-06)


### Performance Improvements

* blueprint cache shared between users ([1748422](https://github.com/equinor/data-modelling-storage-service/commit/174842224bfd9dc82a6759908be71c09008bd11f))


### Build System

* **deps:** bump cryptography from 41.0.5 to 42.0.0 ([9d9d542](https://github.com/equinor/data-modelling-storage-service/commit/9d9d542def860501f214fda648ae1caa0eef0198))
* **deps:** bump fastapi from 0.104.0 to 0.109.1 ([7f17b85](https://github.com/equinor/data-modelling-storage-service/commit/7f17b852a5735845c584ce0d55b01a44fe1dec6e))

## [1.18.3](https://github.com/equinor/data-modelling-storage-service/compare/v1.18.2...v1.18.3) (2024-02-05)


### Bug Fixes

* increase default cache size ([980c149](https://github.com/equinor/data-modelling-storage-service/commit/980c14966cd7017ca6875f505beecd04bfe870db))

## [1.18.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.18.1...v1.18.2) (2024-01-25)


### Code Refactoring

* make resolve document method only return what it is pointing to ([312a744](https://github.com/equinor/data-modelling-storage-service/commit/312a7444d2a23cc5780708ac5903a98f89d2fe93))
* only resolve relevant references ([0fd3f04](https://github.com/equinor/data-modelling-storage-service/commit/0fd3f0454aa8766e0e35faef210f2eb4c775aeba))

## [1.18.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.18.0...v1.18.1) (2024-01-23)


### Code Refactoring

* just return document if depth is zero ([1b7dc20](https://github.com/equinor/data-modelling-storage-service/commit/1b7dc20c19adb7c424315e1e448f54f660f2b045))
* skip create node tree when getting documents ([df39484](https://github.com/equinor/data-modelling-storage-service/commit/df39484f8b9baaa5e25cd72c12b151baf38a9bcf))

## [1.18.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.17.0...v1.18.0) (2024-01-23)


### Features

* more attributes in SIMOS/Meta ([ad39fa8](https://github.com/equinor/data-modelling-storage-service/commit/ad39fa8a6fa312506701ff850d4d007e14af8e3c))


### Bug Fixes

* move to correct folder ([7e455f7](https://github.com/equinor/data-modelling-storage-service/commit/7e455f79d1f17623af600291878db03034d6b823))

## [1.17.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.16.4...v1.17.0) (2024-01-23)


### Features

* url blueprint in core ([32aa750](https://github.com/equinor/data-modelling-storage-service/commit/32aa750d989505eab8e55b92b7975610de1b1c04))

## [1.16.4](https://github.com/equinor/data-modelling-storage-service/compare/v1.16.3...v1.16.4) (2024-01-22)


### Bug Fixes

* better error on not found blueprint ([7a61560](https://github.com/equinor/data-modelling-storage-service/commit/7a615606f46fcd1eda214da926b625fff5b6f7ba))

## [1.16.3](https://github.com/equinor/data-modelling-storage-service/compare/v1.16.2...v1.16.3) (2024-01-17)


### Bug Fixes

* fallback recursive limit should be bigger than common used depth ([a51fa06](https://github.com/equinor/data-modelling-storage-service/commit/a51fa062bedbf2d7e492cf9ae99763f36c4a01bd))

## [1.16.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.16.1...v1.16.2) (2024-01-09)


### Bug Fixes

* remove lingering complex children when changing node type ([3bc7808](https://github.com/equinor/data-modelling-storage-service/commit/3bc780821f29de5443f6af234be9819e06b1fefe))
* tyo in f string ([54e41d8](https://github.com/equinor/data-modelling-storage-service/commit/54e41d81f29d62c378a0188e2ba6f28959461c58))

## [1.16.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.16.0...v1.16.1) (2024-01-05)


### Bug Fixes

* consistent envvar name ([8cd71ed](https://github.com/equinor/data-modelling-storage-service/commit/8cd71eda15e15503611d9b1be402bb9dfc9c9f2b))

## [1.16.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.15.3...v1.16.0) (2024-01-05)


### Features

* validate enums ([ab74bc8](https://github.com/equinor/data-modelling-storage-service/commit/ab74bc82474f9576673a337ec21171c0ef0bb497))


### Code Refactoring

* merge DS and docID in ACL endpoints ([7ba4edf](https://github.com/equinor/data-modelling-storage-service/commit/7ba4edfe43689ade41665cce04fa018f922a5ed4))
* restructure and cleanup core blueprints ([60741af](https://github.com/equinor/data-modelling-storage-service/commit/60741afe86952c8bc10c17b9d7dbc055c026fc9e))


### Build System

* use a data source template and subst envvars ([4094ac4](https://github.com/equinor/data-modelling-storage-service/commit/4094ac4f1eeaa83ffea3389c23d72e231add2ec8))

## [1.15.3](https://github.com/equinor/data-modelling-storage-service/compare/v1.15.2...v1.15.3) (2024-01-03)


### Bug Fixes

* don't explicitly set admin role for service principal ([a129a93](https://github.com/equinor/data-modelling-storage-service/commit/a129a93f32b08154451fbb6501331b786fe7d3fe))
* set filetype and not mime type ([97b96d1](https://github.com/equinor/data-modelling-storage-service/commit/97b96d1836b9f8efaebc64968fdbc9f042c2563b))

## [1.15.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.15.1...v1.15.2) (2023-12-18)


### Bug Fixes

* delete items in list ([01d9fb5](https://github.com/equinor/data-modelling-storage-service/commit/01d9fb578a273657f9e628a146763bfc8be53484))

## [1.15.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.15.0...v1.15.1) (2023-12-18)


### Bug Fixes

* resolve tilde correct ([0853bdc](https://github.com/equinor/data-modelling-storage-service/commit/0853bdc6c9c8df1dd4e9fd09fb99bed17b26f224))

## [1.15.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.14.3...v1.15.0) (2023-12-15)


### Features

* relative references ([9bcca96](https://github.com/equinor/data-modelling-storage-service/commit/9bcca967111bc108682a6aeafc32e4baec4aa021))

## [1.14.3](https://github.com/equinor/data-modelling-storage-service/compare/v1.14.2...v1.14.3) (2023-12-12)


### Bug Fixes

* attribute resolve ([2eaac78](https://github.com/equinor/data-modelling-storage-service/commit/2eaac782ae8ac0d5f86f54834784e586a70faae9))

## [1.14.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.14.1...v1.14.2) (2023-12-09)


### Bug Fixes

* get attributes for address that points to reference ([80f14d8](https://github.com/equinor/data-modelling-storage-service/commit/80f14d8f9a50d22d4b3f80aa0a35de1cfcdcfdaf))
* skip empty storage references while deleting package ([dfa546e](https://github.com/equinor/data-modelling-storage-service/commit/dfa546e43094bd4dd49d400fdd5b6187ba9a594c))

## [1.14.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.14.0...v1.14.1) (2023-12-04)


### Bug Fixes

* bad type format ([d8ba521](https://github.com/equinor/data-modelling-storage-service/commit/d8ba52124bb239e831b470f279ed89ae5d2ef8f9))

## [1.14.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.13.0...v1.14.0) (2023-12-04)


### Features

* role blueprint ([6f38459](https://github.com/equinor/data-modelling-storage-service/commit/6f384591c9f43290bb47ebd928be2d4c623a5cf5))

## [1.13.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.12.0...v1.13.0) (2023-11-30)


### Features

* refreshButton in ViewContif ([beb99a2](https://github.com/equinor/data-modelling-storage-service/commit/beb99a256320492dd73f23578a6f968d617a4765))

## [1.12.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.11.2...v1.12.0) (2023-11-30)


### Features

* partial update ([f0e89fe](https://github.com/equinor/data-modelling-storage-service/commit/f0e89fe294f0b2d6dfeb361a76925c294601c9f2))

## [1.11.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.11.1...v1.11.2) (2023-11-22)


### Bug Fixes

* empty author field if no full name ([e3720f1](https://github.com/equinor/data-modelling-storage-service/commit/e3720f11c60379dbbd8a434af5ade6f0b601095e))

## [1.11.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.11.0...v1.11.1) (2023-11-21)


### Bug Fixes

* bdd tests ([3536c75](https://github.com/equinor/data-modelling-storage-service/commit/3536c75dd8f0506ad01bc58271a2fb7696a7b149))
* refreshbutotnnotserved ([e1073be](https://github.com/equinor/data-modelling-storage-service/commit/e1073becd6b9a2aa04d4c4416b2e84d53e195f6f))

## [1.11.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.10.0...v1.11.0) (2023-11-21)


### Features

* change to false default ([42d2fdd](https://github.com/equinor/data-modelling-storage-service/commit/42d2fdd358c352963270d9e0ba7a82dd47a85d37))


### Build System

* remove publish pypi package ([8099d10](https://github.com/equinor/data-modelling-storage-service/commit/8099d101a3ce046f9c6ed5ebb4fb70b8c9c115ed))

## [1.10.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.9.0...v1.10.0) (2023-11-17)


### Features

* adding refreshable?: bool to uiRecipe ([b121b8a](https://github.com/equinor/data-modelling-storage-service/commit/b121b8aefe4e16ae9da8186c6984ccd87323ecc2))
* rename to showRefreshButton: bool to uiRecipe ([4de1380](https://github.com/equinor/data-modelling-storage-service/commit/4de1380eb74685040b42725a17f125b658d2ef44))


### Bug Fixes

* CreateEntity will now correctly use default, even on optional ([2b0dbe0](https://github.com/equinor/data-modelling-storage-service/commit/2b0dbe07ffd82804fb24f698ad43d267d8de18ea))
* remove abstract from blueprints ([9c98b6e](https://github.com/equinor/data-modelling-storage-service/commit/9c98b6ef57bd3dab79aa5ae82266a6e35e43d0bf))

## [1.9.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.8.1...v1.9.0) (2023-11-14)


### Features

* update entity and namedentity blueprints ([f03059f](https://github.com/equinor/data-modelling-storage-service/commit/f03059f4647b4691d60d4e659a48e1461351fea8))


### Bug Fixes

* address_resolver did not use new datasource name ([55d2051](https://github.com/equinor/data-modelling-storage-service/commit/55d205180932d57dc2bc2581590ba82d121002b5))
* update test to reflect changes in blueprints namedentity ([acb81ae](https://github.com/equinor/data-modelling-storage-service/commit/acb81ae6ede9077a9d0f6f815f469a8d4be8263a))


### Code Refactoring

* resolver ([c96bbc9](https://github.com/equinor/data-modelling-storage-service/commit/c96bbc9ed265ed16ff151cf4077453106e1cf2b1))


### Tests

* validate core SIMOS package ([8668212](https://github.com/equinor/data-modelling-storage-service/commit/866821281e99bbec354c554d101ed0e9638461e6))

## [1.8.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.8.0...v1.8.1) (2023-11-07)


### Bug Fixes

* **node:** Node.node_id() return invalid address to list elements ([4897834](https://github.com/equinor/data-modelling-storage-service/commit/4897834f08dda4829bdb3162d4089c2ce1a16c11))

## [1.8.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.7.1...v1.8.0) (2023-11-06)


### Features

* add optional empty list ([50acd30](https://github.com/equinor/data-modelling-storage-service/commit/50acd306f57b1251f1c92104c615e4641848d7d4))


### Bug Fixes

* add entity information in ValidationExceptions ([a919163](https://github.com/equinor/data-modelling-storage-service/commit/a919163992d9e816b6af4ee6a063f5d47286c20f))
* don't assume same datasouce on resolving next level ([f973686](https://github.com/equinor/data-modelling-storage-service/commit/f97368639d0f3d6f3bddff8aa6774e8447aa9579))
* don't validate primitive attributes of type any ([763ac1a](https://github.com/equinor/data-modelling-storage-service/commit/763ac1ad653d0a795b145c61cfc18c866d8330d8))


### Styles

* run line length formatting ([91718cf](https://github.com/equinor/data-modelling-storage-service/commit/91718cf5d07d6eacf9119688323f5240c64f21c4))


### Miscellaneous Chores

* bump FastAPI and gunicorn ([2e52e7a](https://github.com/equinor/data-modelling-storage-service/commit/2e52e7a936239a265322153d18e2eb8e98e535bc))
* bump python -&gt; 3.12 ([340a4a4](https://github.com/equinor/data-modelling-storage-service/commit/340a4a463db2619287f663961747ab425c4d4fec))
* fix mypy errors ([71d1305](https://github.com/equinor/data-modelling-storage-service/commit/71d1305cd942e5468e53f85151a7f7fb90c77725))
* fix ruff linting violations ([0848024](https://github.com/equinor/data-modelling-storage-service/commit/0848024e660793cf928cfff1001db07999f72c98))


### Build System

* bump openapi generator ([01e8d38](https://github.com/equinor/data-modelling-storage-service/commit/01e8d38c7c804bdd8850e973ec0e433554d1e82d))
* replace black, pycln, isort, flake8, bandit, with RUFF ([f8e2759](https://github.com/equinor/data-modelling-storage-service/commit/f8e275975d4c8da104905bdb9318429b61b5b333))

## [1.7.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.7.0...v1.7.1) (2023-10-27)


### Bug Fixes

* defer checking of duplicate name in empty package references ([0e69b45](https://github.com/equinor/data-modelling-storage-service/commit/0e69b45fc8ab1fec961155fecd2dd823f9a09aad))

## [1.7.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.6.5...v1.7.0) (2023-10-27)


### Features

* get_attribute able to resolve references ([11a1464](https://github.com/equinor/data-modelling-storage-service/commit/11a14640a62004a6d7cf205824aa3893a40d6405))


### Bug Fixes

* **export:** add proper error response on export ++ minor issues ([7d32dfe](https://github.com/equinor/data-modelling-storage-service/commit/7d32dfe76cfe3f3c99f4e7acab1f9b57c3e1c3c7))

## [1.6.5](https://github.com/equinor/data-modelling-storage-service/compare/v1.6.4...v1.6.5) (2023-10-27)


### Bug Fixes

* transform entities into references only in case of storage uncontained ([9f919af](https://github.com/equinor/data-modelling-storage-service/commit/9f919afcb40a02ad3efa5c2f8e6fd6eb6cd5a9f5))

## [1.6.4](https://github.com/equinor/data-modelling-storage-service/compare/v1.6.3...v1.6.4) (2023-10-16)


### Miscellaneous Chores

* **deps:** bump cryptography from 41.0.3 to 41.0.4 ([434c750](https://github.com/equinor/data-modelling-storage-service/commit/434c750121599f1c010637f5dfb4b944c327e5fa))


### Code Refactoring

* change default value to 0 for depth ([e1829ed](https://github.com/equinor/data-modelling-storage-service/commit/e1829edda6e13751d1ec9df5842509d624e4a5eb))


### Build System

* **deps-dev:** bump gitpython from 3.1.32 to 3.1.37 ([3220966](https://github.com/equinor/data-modelling-storage-service/commit/32209665292c3ddd38601038c55845108ce76a66))
* **deps:** bump urllib3 from 2.0.4 to 2.0.6 ([3d2e0e0](https://github.com/equinor/data-modelling-storage-service/commit/3d2e0e02d947b861ae2ea74dd7982944bd8263a0))

## [1.6.3](https://github.com/equinor/data-modelling-storage-service/compare/v1.6.2...v1.6.3) (2023-10-12)


### Bug Fixes

* A validation check should raise a ValidationException ([5991fc6](https://github.com/equinor/data-modelling-storage-service/commit/5991fc6ab0c29ba1155985a376d0d45acb128519))
* update entities inside packages ([08a370d](https://github.com/equinor/data-modelling-storage-service/commit/08a370d08b1d16b463898c8a7f52c8540bf7d066))

## [1.6.2](https://github.com/equinor/data-modelling-storage-service/compare/v1.6.1...v1.6.2) (2023-10-12)


### Code Refactoring

* make author optional ([4110d17](https://github.com/equinor/data-modelling-storage-service/commit/4110d170c681301991b73f1245cda978965dab74))


### Tests

* did it for add_document ([a53e160](https://github.com/equinor/data-modelling-storage-service/commit/a53e160d8a30552e15b40938e818faa39034a07d))
* did it for car rental blueprints ([0a527d9](https://github.com/equinor/data-modelling-storage-service/commit/0a527d9cb0e980d09faaa272122997fa5a4e472c))
* did it for rest of blueprints ([65b0806](https://github.com/equinor/data-modelling-storage-service/commit/65b0806c28b922905a74f09abd9a9c9ef4e986be))
* did it for validators ([62c0cb0](https://github.com/equinor/data-modelling-storage-service/commit/62c0cb0f74923ad5cc7e2d1b960236543a25171a))
* finished moving storage recipes down ([9ac8adf](https://github.com/equinor/data-modelling-storage-service/commit/9ac8adf272646b1cb4118c18b87663979bdd9d9c))
* made extension actually work ([746683a](https://github.com/equinor/data-modelling-storage-service/commit/746683ad378fc2c0fffccd6acb61c2ff85bb4fbd))
* refactor complex arrays ([10c4529](https://github.com/equinor/data-modelling-storage-service/commit/10c4529a8f3fe69074b639f5c19d63f498bb8ebd))
* removed all common storage recipes ([6f99e51](https://github.com/equinor/data-modelling-storage-service/commit/6f99e515625926a063e23ffb33cbf09fbe910957))

## [1.6.1](https://github.com/equinor/data-modelling-storage-service/compare/v1.6.0...v1.6.1) (2023-10-10)


### Bug Fixes

* update default initial uiRecipe from attribute selector ([6c4da8d](https://github.com/equinor/data-modelling-storage-service/commit/6c4da8da89c2b94b96ae0a7c6c25a732070e6bff))

## [1.6.0](https://github.com/equinor/data-modelling-storage-service/compare/v1.5.0...v1.6.0) (2023-10-09)


### Features

* roles attribute on view config ([b6ebf9e](https://github.com/equinor/data-modelling-storage-service/commit/b6ebf9ec1127e58d4b688988dce0f8743e1c87b3))


### Bug Fixes

* adding init to fix a import error in pat ([bd42ce0](https://github.com/equinor/data-modelling-storage-service/commit/bd42ce0b860e09ad25d3ef660db2b870457600b6))
* adjust depth to avoid resolve more than needed ([29d9c85](https://github.com/equinor/data-modelling-storage-service/commit/29d9c85fae1c751db6454294e821c08e258ab576))
* cast to v4 ([d1bd3f2](https://github.com/equinor/data-modelling-storage-service/commit/d1bd3f2f51cd391dc5ba40bc90531da012e65a88))
* not throw on empty role assignments ([e4ce92a](https://github.com/equinor/data-modelling-storage-service/commit/e4ce92a8081a54e15f72d8460a4f1dde165509a4))
* remove $ from uuid to make it work ([c47b74e](https://github.com/equinor/data-modelling-storage-service/commit/c47b74e5da42deace2ea8d81866e424501e930f0))
* remove item from required list attribute ([91c774b](https://github.com/equinor/data-modelling-storage-service/commit/91c774b0706a54ba9534a5e1ec7649a0c58acc69))
* returns Bad Request on invalid id ([138db67](https://github.com/equinor/data-modelling-storage-service/commit/138db676bd71eefc1c3ba92d3235ce93168190c2))


### Documentation

* how to run bdd file ([8417e03](https://github.com/equinor/data-modelling-storage-service/commit/8417e03bcb26bce2085c66e33c5d54419fdd823d))


### Code Refactoring

* add parameters to blueprint_provider so that it can be tested ([6af84f0](https://github.com/equinor/data-modelling-storage-service/commit/6af84f002b6e6db08b63da0db4ca3e0a8ebebcb0))
* also move into entity ([b131aa5](https://github.com/equinor/data-modelling-storage-service/commit/b131aa5127103805b0e985da3eeea8ce2d04354f))
* delete dot notation and tests, unused ([0cced85](https://github.com/equinor/data-modelling-storage-service/commit/0cced856dc74f5f8f047e2f72f555fa0e104bf55))
* docstrings ([6c16312](https://github.com/equinor/data-modelling-storage-service/commit/6c163124f57861c8b9917b664ae654e87648e8fa))
* get and print diff ([1790f6a](https://github.com/equinor/data-modelling-storage-service/commit/1790f6a96b7ba3548e1dba4649ddc1feef0b5ea0))
* merge ([01f3b6b](https://github.com/equinor/data-modelling-storage-service/commit/01f3b6b271ba0f52f633f02babca26e4c7c5adf7))
* move and stuff ([7b4f07d](https://github.com/equinor/data-modelling-storage-service/commit/7b4f07df411231188fbdf6551c965f8000c6097c))
* move create pat into use case ([c2c0868](https://github.com/equinor/data-modelling-storage-service/commit/c2c0868f2d73aba5b43edcc978a3b58dc290937c))
* move date-time-checking into the auth method, and not in the extract user method ([6861bd6](https://github.com/equinor/data-modelling-storage-service/commit/6861bd678c0515738ced70a4cfaf9fd1248e0752))
* move into providers folder ([470c08c](https://github.com/equinor/data-modelling-storage-service/commit/470c08ceaaf3c327fd57ef7d885217aa9cb74ccf))
* move into screaming folders ([7013414](https://github.com/equinor/data-modelling-storage-service/commit/7013414cfaf868c2741519ee673c29f6257e06dd))
* move into use cases ([87a0d2d](https://github.com/equinor/data-modelling-storage-service/commit/87a0d2d974b099883e2a18efc317b3ab3cab81c4))
* move test helpers under src/tests ([dd9fbe3](https://github.com/equinor/data-modelling-storage-service/commit/dd9fbe36f6ef4a430b2381318d1150fb0bdc8845))
* rebase ([322e838](https://github.com/equinor/data-modelling-storage-service/commit/322e8388cd1d23cf5e947ad2cf2c42235e8e5f65))
* remove get and print diff ([00c8c37](https://github.com/equinor/data-modelling-storage-service/commit/00c8c37d00d7013a70c9e4efe8334365204313bf))
* remove last traces of 'update_uncontained' ([25eac2f](https://github.com/equinor/data-modelling-storage-service/commit/25eac2f3c59ec6350a2b9a9de766049b4bf1fc37))
* remove more unused methods for tree node ([b1808fe](https://github.com/equinor/data-modelling-storage-service/commit/b1808feb5bf4039996428f8673904952fc1e68c9))
* remove uneccesary comment ([192395b](https://github.com/equinor/data-modelling-storage-service/commit/192395b4e8e1c603c316b4eee12e8baceff2c5f0))
* remove unused ([0b1c8c7](https://github.com/equinor/data-modelling-storage-service/commit/0b1c8c7c305ce9365349c87a3643aef008d988e0))
* remove unused methods in tree node ([40f31b2](https://github.com/equinor/data-modelling-storage-service/commit/40f31b20e4768773ed66a4a3cac2b62e5b01a79c))
* remove unused stuff in create_entity.py ([d46924f](https://github.com/equinor/data-modelling-storage-service/commit/d46924fc0c0b27935dca0e4fb5d57af505354ecb))
* rename file to blueprint_provider ([004a8f2](https://github.com/equinor/data-modelling-storage-service/commit/004a8f2cb727027fafe2d0bf874327e42da43cd3))
* rename method to something more readable ([c9c59db](https://github.com/equinor/data-modelling-storage-service/commit/c9c59dbbe5d8774a37d2b324014f067bed04807a))
* rename zip to zip file client ([5006d9a](https://github.com/equinor/data-modelling-storage-service/commit/5006d9a88d94d442eb21715b036bbb506f3ac679))
* simpler constructor ([9ee5a19](https://github.com/equinor/data-modelling-storage-service/commit/9ee5a1945574916121e37d13007bc0d058483474))
* stuf ([93b2ff9](https://github.com/equinor/data-modelling-storage-service/commit/93b2ff9856f70bf06b08c49aaccceaae431b01fe))
* test ([6a55035](https://github.com/equinor/data-modelling-storage-service/commit/6a55035c771d66dfc764e47b63e1844f014cb4dd))


### Tests

* add bestFriend to person ([a4bbe82](https://github.com/equinor/data-modelling-storage-service/commit/a4bbe828baf236579b6945a1febcae06f5ada129))
* added test for access control, also a comment ([b93f6ef](https://github.com/equinor/data-modelling-storage-service/commit/b93f6ef24c82f26a6e27099af68b4828703038d1))
* added test for access control, also a comment ([7e9abe0](https://github.com/equinor/data-modelling-storage-service/commit/7e9abe0f3598bee7b903d683e31acc5627da0c19))
* added test for the USER class ([81e5a1c](https://github.com/equinor/data-modelling-storage-service/commit/81e5a1c856909f2c7b03bda0f58f4008532e4f6d))
* added tests for pat data, also fixed type hinting to be correct ([d1192b9](https://github.com/equinor/data-modelling-storage-service/commit/d1192b9ae1e4d7c8365510a875d6fedd0e01ee66))
* added tests for the access control list ([317a57e](https://github.com/equinor/data-modelling-storage-service/commit/317a57ee75237106cd28b1564a39296e8148dba8))
* adding more tests for the access level comparison, and fix typo in name ([416ddd0](https://github.com/equinor/data-modelling-storage-service/commit/416ddd02b811290483da166f14dea859557bf2e0))
* also changed name of other methods ([3757e9f](https://github.com/equinor/data-modelling-storage-service/commit/3757e9f49bc090125b9c19a6fe927e4aa0c2d2a0))
* also changed name of other methods ([b3dbc5a](https://github.com/equinor/data-modelling-storage-service/commit/b3dbc5a14e845a6be7f37352024db735154e5466))
* better name for test method ([f4ee77f](https://github.com/equinor/data-modelling-storage-service/commit/f4ee77fa4807b218318a67d8c0dbb288fd465c6d))
* better name for testing method ([657334b](https://github.com/equinor/data-modelling-storage-service/commit/657334b1b803243ad6876e1404c64a6255386a7e))
* chagned one file tree node helpers to use the general mocker instead ([bba6481](https://github.com/equinor/data-modelling-storage-service/commit/bba64819a6fc719b3a4c6efbf631b6dc1eefb624))
* chagned one file tree node helpers to use the general mocker instead ([fa69474](https://github.com/equinor/data-modelling-storage-service/commit/fa69474ce355cc20478cdcb4b12320207cd6636f))
* clean up a bit for readability ([4a0470d](https://github.com/equinor/data-modelling-storage-service/commit/4a0470d5fb7e59c411b513f9147786389d3110f6))
* finish test tree node helpers ([c7d0974](https://github.com/equinor/data-modelling-storage-service/commit/c7d0974e42916d3baa580b0edc1a39a7bf87ee21))
* finish test_tree_node_to_dict refactor ([5d0a572](https://github.com/equinor/data-modelling-storage-service/commit/5d0a57211dff8e7eb58920ff7d01e85889adfd2b))
* fix namedEntity should be person ([7f25cb1](https://github.com/equinor/data-modelling-storage-service/commit/7f25cb1b0085d381de32415a516c47874c369733))
* for some test, moving blueprints 'down' ([59e74d8](https://github.com/equinor/data-modelling-storage-service/commit/59e74d87f95bb5b23ac591fbc367e33f4d460f74))
* make is simpler, clear away code ([95ddcb7](https://github.com/equinor/data-modelling-storage-service/commit/95ddcb7b476f528f06d7c2f13ad110bf1c7d4686))
* make the node helpers more explicit also ([baf6501](https://github.com/equinor/data-modelling-storage-service/commit/baf6501606eb5d0d52503b28a5c33862d8837663))
* merge ([149cd83](https://github.com/equinor/data-modelling-storage-service/commit/149cd836d24934bce1eebc633b1666775481c3c1))
* mock storage recipe provicer data-less ([12d75ca](https://github.com/equinor/data-modelling-storage-service/commit/12d75ca157336f240db6f45e8185e0e636497f4b))
* move blueprints 'down' into reference use case ([aafa20b](https://github.com/equinor/data-modelling-storage-service/commit/aafa20bbfa7d2d3765244c07bda64f7b9450a71f))
* move blueprints 'down' to validator ([8ec1368](https://github.com/equinor/data-modelling-storage-service/commit/8ec13687e9554e7762bcc71ebc6aae2c89c702f0))
* move into folders to reflect changes done in src/ ([9ab12ba](https://github.com/equinor/data-modelling-storage-service/commit/9ab12bac32dd31a867c2742a74e287fadbd7735b))
* move into setup ([daaaea2](https://github.com/equinor/data-modelling-storage-service/commit/daaaea2efa3b6ceb09f0aeccdf7bfaae32bd8d25))
* move raising no credentials out ([412a59f](https://github.com/equinor/data-modelling-storage-service/commit/412a59fe6ea6f64cee88d08e567a824a777edbbb))
* move responsability up ([fd572e3](https://github.com/equinor/data-modelling-storage-service/commit/fd572e377aba237ab60c84b8ba9a08689b35db6c))
* moved down for create_entity ([bbf3e76](https://github.com/equinor/data-modelling-storage-service/commit/bbf3e76246aaa25ff39bd5b84421d0baf9a3588c))
* moving default into classes ([b482a67](https://github.com/equinor/data-modelling-storage-service/commit/b482a677beed57607506b7d7d1c645cc8a70478a))
* must specify path to storage recipes location ([4f566cd](https://github.com/equinor/data-modelling-storage-service/commit/4f566cd628cd08ab34eca30d6a39422e13665aa5))
* rebase 1 ([fafa326](https://github.com/equinor/data-modelling-storage-service/commit/fafa3269d1dc82ed2f1c365dc99e348813c8c2d0))
* rebasing ([0f00f74](https://github.com/equinor/data-modelling-storage-service/commit/0f00f74068a05ae84ad5c06a31ea0273eeffd27f))
* refactor tree node update further to make it more clean and readable ([8ab3ab8](https://github.com/equinor/data-modelling-storage-service/commit/8ab3ab81ce69f8d0c61ff511ecd23add08a8319e))
* remove aclc ([caeeeaf](https://github.com/equinor/data-modelling-storage-service/commit/caeeeaf63e64ecab8c929a0bd473f639fc7c19a7))
* remove all common blueprints, not used ([53bd8b8](https://github.com/equinor/data-modelling-storage-service/commit/53bd8b829da2b8efffe4a1a9b4d77e8642c0f9a5))
* remove duplicate mockers ([9418e40](https://github.com/equinor/data-modelling-storage-service/commit/9418e40eeb9d2af8cf60fcc4f9055679c79979cb))
* remove roles ([bfb065f](https://github.com/equinor/data-modelling-storage-service/commit/bfb065f141d6c5d43abe471669a05bcbfbe8719d))
* remove uneccesary parameters ([2691d42](https://github.com/equinor/data-modelling-storage-service/commit/2691d4213e479967547a5911bc4608a268380af0))
* removed duplicate methods testing the same thing, but with different blueprints ([962937b](https://github.com/equinor/data-modelling-storage-service/commit/962937bee02d7a78080d114eaa9ca5e7413c4502))
* removed empty optional descriptions everywhere in the test_remove ([5ac9744](https://github.com/equinor/data-modelling-storage-service/commit/5ac974418d5d06763634f223dc1e1c61cbc967fb))
* removed unused blueprint reference after deleted test ([60871a9](https://github.com/equinor/data-modelling-storage-service/commit/60871a92fed182b982dac9002dddab838906a853))
* replaced method-in-method with method-in-class ([9d41545](https://github.com/equinor/data-modelling-storage-service/commit/9d4154550ca405a58621a766448311ebbdf83b76))
* started replacing custom with general mocker ([a09b811](https://github.com/equinor/data-modelling-storage-service/commit/a09b8116cb401a1d6ebf3e62f35022afe2f9a338))
* started replacing custom with general mocker ([5e87072](https://github.com/equinor/data-modelling-storage-service/commit/5e8707205919590a11552c92e35551aad35c6d2b))
* test for address class and classMethods ([785224f](https://github.com/equinor/data-modelling-storage-service/commit/785224fadb8b949c4169d4fd9a4d8b3b20882841))
* test for the user default() ([5c7216b](https://github.com/equinor/data-modelling-storage-service/commit/5c7216b7aeec8103c9a51062c7dbc46c794406c0))
* test utils ([321fc69](https://github.com/equinor/data-modelling-storage-service/commit/321fc693eabe94ef50abbcd78d6f7da16f8b482a))
* testing removing of roles ([89a5fe5](https://github.com/equinor/data-modelling-storage-service/commit/89a5fe53ce0693bf29894f342b3c341d466c55ff))
* tests for the new default acl ([e72a888](https://github.com/equinor/data-modelling-storage-service/commit/e72a8889ef074bc391aa21d548193ec3af3b688d))
* tree node to ref dict ([ee7fa49](https://github.com/equinor/data-modelling-storage-service/commit/ee7fa4910b8040d25b2bac6b0766b6b752f7d802))
* trying git stuff ([01402b5](https://github.com/equinor/data-modelling-storage-service/commit/01402b594e9339ea89c4f6fa865e096addc3ec35))
* unit tests for is_reference ([f40e7da](https://github.com/equinor/data-modelling-storage-service/commit/f40e7da82dbeae95239d7158ef56287c19bcf293))
* unit tests for sort dtos ([8ba2d59](https://github.com/equinor/data-modelling-storage-service/commit/8ba2d5910ff68df99f2257421d2a4855a15ed7e5))

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
