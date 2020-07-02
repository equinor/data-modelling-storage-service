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
 * @interface InlineObject4
 */
export interface InlineObject4 {
    /**
     * 
     * @type {string}
     * @memberof InlineObject4
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof InlineObject4
     */
    parentId?: string | null;
    /**
     * 
     * @type {string}
     * @memberof InlineObject4
     */
    description?: string | null;
    /**
     * 
     * @type {string}
     * @memberof InlineObject4
     */
    documentId: string;
}

export function InlineObject4FromJSON(json: any): InlineObject4 {
    return InlineObject4FromJSONTyped(json, false);
}

export function InlineObject4FromJSONTyped(json: any, ignoreDiscriminator: boolean): InlineObject4 {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': json['name'],
        'parentId': !exists(json, 'parentId') ? undefined : json['parentId'],
        'description': !exists(json, 'description') ? undefined : json['description'],
        'documentId': json['documentId'],
    };
}

export function InlineObject4ToJSON(value?: InlineObject4 | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'parentId': value.parentId,
        'description': value.description,
        'documentId': value.documentId,
    };
}


