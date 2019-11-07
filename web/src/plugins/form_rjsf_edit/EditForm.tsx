import React from 'react'
import Form from 'react-jsonschema-form'
import { Blueprint, PluginProps } from '../types'
import { createFormConfigs, FormConfig } from './CreateConfig'
import { findRecipe, setupTypeAndRecipe } from '../pluginUtils'
import { AttributeWidget } from '../form-rjsf-widgets/Attribute'
import { ReadOnly } from '../form-rjsf-widgets/ReadOnly'

interface Props extends PluginProps {
  onSubmit: (data: any) => void
}

export const EditPlugin = (props: Props) => {
  const uiRecipe = findRecipe(props.blueprint, props.name)
  const config: FormConfig = createFormConfigs(props, uiRecipe)
  const formData = config.data
  return (
    <div style={{ marginBottom: 20 }}>
      <Form
        schema={config.template}
        formData={formData || {}}
        uiSchema={config.uiSchema || {}}
        fields={{
          attribute: AttributeWidget,
          hidden: () => <div />,
          readonly: ReadOnly,
        }}
        onChange={formData => {
          console.log(formData)
        }}
        onSubmit={props.onSubmit}
      />
    </div>
  )
}

/**
 * Parent is used to generate defaults, a description attributes has other defaults
 * than a type attribute or boolean attribute.
 *
 * @param parent Blueprint
 */
export const getWidgetBlueprint = (
  pluginProps: PluginProps
): Blueprint | null => {
  // process once.
  const { uiAttributeType } = setupTypeAndRecipe(pluginProps)
  if (pluginProps && uiAttributeType && uiAttributeType.attributes) {
    return uiAttributeType
  }
  console.warn(
    'attributes blueprint for this widget is missing. Nothing is rendered.'
  )
  return null
}
