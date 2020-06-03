/* tslint:disable */
/* eslint-disable */
/**
 * Data Modelling Storage Service API
 * Data storage service for DMT
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface InlineObject
 */
export interface InlineObject {
    /**
     * 
     * @type {string}
     * @memberof InlineObject
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof InlineObject
     */
    parentId: string;
    /**
     * 
     * @type {string}
     * @memberof InlineObject
     */
    type: string;
    /**
     * 
     * @type {string}
     * @memberof InlineObject
     */
    attribute: string;
}

export function InlineObjectFromJSON(json: any): InlineObject {
    return InlineObjectFromJSONTyped(json, false);
}

export function InlineObjectFromJSONTyped(json: any, ignoreDiscriminator: boolean): InlineObject {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': json['name'],
        'parentId': json['parentId'],
        'type': json['type'],
        'attribute': json['attribute'],
    };
}

export function InlineObjectToJSON(value?: InlineObject | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'parentId': value.parentId,
        'type': value.type,
        'attribute': value.attribute,
    };
}


