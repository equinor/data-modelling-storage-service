import { BlueprintAttributeType } from '../plugins/types'

export class BlueprintAttribute {
  private attr: BlueprintAttributeType
  constructor(attr: BlueprintAttributeType) {
    this.attr = attr
  }

  public getName(): string {
    return this.attr.name
  }

  public isArray() {
    return this.attr.dimensions && this.attr.dimensions === '*'
  }

  public static isArray(value: string) {
    return value === '*'
  }

  public isPrimitive(): boolean {
    //todo use AttributeTypes enum, available in the blueprint.
    return ['string', 'number', 'integer', 'number', 'boolean'].includes(
      this.attr.type
    )
  }
}
