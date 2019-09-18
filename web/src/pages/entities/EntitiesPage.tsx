import React, { useEffect, useReducer } from 'react'
import DocumentTree, { RenderProps } from '../common/tree-view/DocumentTree'
import EntitiesReducer, {
  DocumentActions,
  initialState,
} from '../common/DocumentsReducer'
import { DataSourceType, DmtApi } from '../../api/Api'
import axios from 'axios'
import { EntityNode } from './nodes/EntityNode'
import { FolderNode } from './nodes/FolderNode'
import Header from '../../components/Header'
import { Wrapper } from '../blueprints/BlueprintsPage'
import Button from '../../components/Button'
import { DataSourceNode } from '../blueprints/nodes/DataSourceNode'
import { RootFolderNode } from './nodes/RootFolderNode'
import { TreeNodeData } from '../../components/tree-view/Tree'

const api = new DmtApi()

function getNodeComponent(treeNodeData: TreeNodeData) {
  switch (treeNodeData.nodeType) {
    case 'folder':
      if (treeNodeData.isRoot) {
        return RootFolderNode
      } else {
        return FolderNode
      }
    case 'file':
      return EntityNode
    case 'datasource':
      return DataSourceNode
    default:
      return (props: RenderProps) => <div>{props.treeNodeData.title}</div>
  }
}

export default () => {
  const [state, dispatch] = useReducer(EntitiesReducer, initialState)
  // const pageMode = state.pageMode

  //not use useFetch hook because response should be dispatched to the reducer.
  useEffect(() => {
    //avoid unnecessary fetch.
    if (!state.dataSources.length) {
      axios(api.dataSourcesGet(DataSourceType.Entities))
        .then((res: any) => {
          dispatch(DocumentActions.addDatasources(res.data))
        })
        .catch((e: any) => {
          console.log(e)
        })
    }
  }, [state.dataSources.length])

  return (
    <Wrapper>
      <Header style={{ marginBottom: 20 }}>
        <Button>Add datasource</Button>
      </Header>
      <br />
      <DocumentTree
        render={(renderProps: RenderProps) => {
          const { treeNodeData, addNode, updateNode } = renderProps
          const NodeComponent = getNodeComponent(treeNodeData)
          return (
            <NodeComponent
              addNode={addNode}
              updateNode={updateNode}
              treeNodeData={treeNodeData}
              state={state}
              dispatch={dispatch}
            />
          )
        }}
        dataSources={state.dataSources}
      />
    </Wrapper>
  )
}
