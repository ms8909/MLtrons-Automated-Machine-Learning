import { projectConstants } from '../_constants';

export function groups(state = {}, action) {

  switch (action.type) {
    case projectConstants.TAGS_REQUEST:
      return Object.assign({}, state, {
        tags_loading: true,
      });
    case projectConstants.TAGS_SUCCESS:
      return Object.assign({}, state, {
        tags: action.tags,
        tags_loading: false,

      });
    case projectConstants.TAGS_FAILURE:
      return Object.assign({}, state, {
        tags_error: action.error,
        tags_loading: false,
      });
    case projectConstants.DURATION_REQUEST:
      return Object.assign({}, state, {
        duration_loading: true,
      });
    case projectConstants.DURATION_SUCCESS:
      return Object.assign({}, state, {
        durations: action.durations,
        duration_loading: false,
      });
    case projectConstants.DURATON_FAILURE:
      return Object.assign({}, state, {
        duration_error: action.error,
        duration_loading: false,
      });
    case projectConstants.ADD_GROUP_REQUEST:
      return Object.assign({}, state, {
        add_request: true,
      });
    case projectConstants.ADD_GROUP_SUCCESS:
      return Object.assign({}, state, {
        created: action.created,
        add_request: false,
      });
    case projectConstants.ADD_GROUP_FAILURE:
      return Object.assign({}, state, {
        add_error: action.error,
        add_request: false,
      });
    case projectConstants.SEARCH_TAG_REQUEST:
      return Object.assign({}, state, {
        tag_search: true,
      });
    case projectConstants.SEARCH_TAG_SUCCESS:
      return Object.assign({}, state, {
        s_tags: action.tags,
        tag_search: false,
      });
    case projectConstants.SEARCH_TAG_FAILURE:
      return Object.assign({}, state, {
        add_error: action.error,
        tag_search: false,
      });
    case projectConstants.FILTER_GROUP_REQUEST:
      return Object.assign({}, state, {
        groups_filter: true,
      });
    case projectConstants.FILTER_GROUP_SUCCESS:
      return Object.assign({}, state, {
        groups: action.groups,
        groups_filter: false,
      });
    case projectConstants.SEARCH_TAG_FAILURE:
      return Object.assign({}, state, {
        filter_error: action.error,
        groups_filter: false,
      });
    case projectConstants.GET_GROUP_REQUEST:
      return Object.assign({}, state, {
        get_group: true,
      });
    case projectConstants.GET_GROUP_SUCCESS:
      return Object.assign({}, state, {
        group: action.groups,
        get_group: false,
      });
    case projectConstants.GET_GROUP_FAILURE:
      return Object.assign({}, state, {
        group_error: action.error,
        get_group: false,
      });
     case projectConstants.GET_GROUP_MEMBERS_REQUEST:
      return Object.assign({}, state, {
        request: true,
      });
    case projectConstants.GET_GROUP_MEMBERS_SUCCESS:
      return Object.assign({}, state, {
        members: action.members,
        request: false,
      });
    case projectConstants.GET_GROUP_MEMBERS_FAILURE:
      return Object.assign({}, state, {
        error: action.error,
        request: false,
      });

    case projectConstants.GET_GROUP_CHAT_REQUEST:
      return Object.assign({}, state, {
        request: true,
      });
    case projectConstants.GET_GROUP_CHAT_SUCCESS:
      return Object.assign({}, state, {
        chats: action.chats,
        request: false,
      });
    case projectConstants.GET_GROUP_CHAT_FAILURE:
      return Object.assign({}, state, {
        error: action.error,
        request: false,
      });
    case projectConstants.ADD_CHAT_REQUEST:
      return Object.assign({}, state, {
        request: true,
      });
    case projectConstants.ADD_CHAT_SUCCESS:
      return Object.assign({}, state, {
        chat_created: action.created,
        request: false,
      });
    case projectConstants.ADD_GROUP_FAILURE:
      return Object.assign({}, state, {
        error: action.error,
        request: false,
      });
    case projectConstants.GET_GROUP_BY_USER_REQUEST:
      return Object.assign({}, state, {
        request: true,
      });
    case projectConstants.GET_GROUP_BY_USER_SUCCESS:
      return Object.assign({}, state, {
        my_groups: action.groups,
        request: false,
      });
    case projectConstants.GET_GROUP_BY_USER_FAILURE:
      return Object.assign({}, state, {
        error: action.error,
        request: false,
      });
    case projectConstants.GET_ALL_USERS_SUCCESS:
      return Object.assign({}, state, {
        all_users: action.users,
      });
    case projectConstants.GET_ALL_JOBTITLES_SUCCESS:
      return Object.assign({}, state, {
        all_jobs: action.titles,
      });
    case projectConstants.GET_ADD_MEMBER_SUCCESS:
      return Object.assign({}, state, {
        created: action.created,
      });
    case projectConstants.GET_ADD_TAG_SUCCESS:
      return Object.assign({}, state, {
        created: action.created,
      });
    case projectConstants.DELETE_MEMBER_SUCCESS:
      return Object.assign({}, state, {
        deleted: action.deleted,
      });
    case projectConstants.PROMOTE_MEMBER_SUCCESS:
      return Object.assign({}, state, {
        updated: action.updated,
      });
    case projectConstants.GET_PROJECT_SUCCESS:
      return Object.assign({}, state, {
        projects: action.projects,
      });
    case projectConstants.GET_ONE_PROJECT_SUCCESS:
      return Object.assign({}, state, {
        project: action.project,
      });
    case projectConstants.GET_META_TYPE_SUCCESS:
      return Object.assign({}, state, {
        meta_type: action.meta_type,
      });
    case projectConstants.GET_META_ROLE_SUCCESS:
      return Object.assign({}, state, {
        meta_role: action.meta_role,
      });
    case projectConstants.GET_META_IMPUTATION_SUCCESS:
      return Object.assign({}, state, {
        meta_imputation: action.meta_imputation,
      });
    case projectConstants.GET_PROBLEM_TYPE_SUCCESS:
      return Object.assign({}, state, {
        problem_type: action.problem_type,
      });
    case projectConstants.GET_TIME_TYPE_SUCCESS:
      return Object.assign({}, state, {
        time_type: action.time_type,
      });
    case projectConstants.GET_TRAINING_DETAIL_SUCCESS:
      return Object.assign({}, state, {
        training_detail: action.training,
      });
    case projectConstants.GET_TRAINING_METRIC_SUCCESS:
      return Object.assign({}, state, {
        metric: action.metric,
      });
    case projectConstants.GET_TRAINING_MODELS_SUCCESS:
      return Object.assign({}, state, {
        models: action.models,
      });
    case projectConstants.GET_ACCURACY_SUCCESS:
      return Object.assign({}, state, {
        accuracy: action.resp,
      });
    case projectConstants.GET_ROC_SUCCESS:
      return Object.assign({}, state, {
        roc: action.resp,
      });
    case projectConstants.GET_BLUE_PRINT_SUCCESS:
      return Object.assign({}, state, {
        blue_print: action.resp,
      });
    case projectConstants.GET_FEATURE_IMPORTANCE_SUCCESS:
        data = action.resp;
        if(action.resp!=undefined){
            data = data.data;
            delete data.graph_type;
        }
      return Object.assign({}, state, {
        feature_importance: data,
      });
    case projectConstants.GET_LOSS_INTERACTION_SUCCESS:
      return Object.assign({}, state, {
        loss_interaction: action.resp,
      });
    case projectConstants.GET_ACTUAL_PREDICTION_SUCCESS:
      return Object.assign({}, state, {
        actual_prediction: action.resp,
      });
    case projectConstants.SET_SELECTED_SUCCESS:
      return Object.assign({}, state, {
        selected_dataset: action.selected_dataset,
        selected_metas: action.selected_metas,
      });
    case projectConstants.GET_PROGRESS_SUCCESS:
      return Object.assign({}, state, {
        progress: action.progress,
      });
    case projectConstants.GET_TASK_PROGRESS:
      return Object.assign({}, state, {
        task: action.task,
      });
    case projectConstants.CLEAR_META_STATE:
      return Object.assign({}, state, {
        metas: [],
        tables: [],
      });
    case projectConstants.GET_DEPLOYED_MODEL:
      return Object.assign({}, state, {
          deployed: action.model,
      });

      case projectConstants.GET_TESTING_GRAPH:
          return Object.assign({}, state, {
              graph: action.graph,
          });
    case projectConstants.GET_TESTING_SET:
      let {testing, deployed} = state;
      if(testing == undefined)testing=[];
      testing.push(action.testing);
      let t = false;
      if(deployed!=undefined && deployed.length>0){
        for(let test of testing){
          if(deployed[0].model_d.training.processed_file_d.parent == null){
            if(test[0].data == deployed[0].model_d.training.processed_file)t=true;
          }
          else{
            let c = 0;
            for(let parent of deployed[0].model_d.training.processed_file_d.parent.dataset){
              if(parent == test[0].data)c++;
            }
            if(c == testing.length)t=true;
          }
        }
      }
      return Object.assign({}, state, {
        testing: testing,
        testable: t,
      });
    case projectConstants.GET_META_SUCCESS:
      let {metas, tables} = state;
      if(metas == undefined)metas=[];
      if(tables == undefined)tables=[];
      let offset = 350 * tables.length
      metas.push(action.meta);
      let fields = [];
      for(let column of action.meta.meta){
        fields.push({'name': column.column_name})
      }
      let location;
      if (action.meta.dataset.loc!=undefined)location = action.meta.dataset.loc;
      else location = `${offset} 0`;
      let table = { key: action.meta.dataset.name.split('.')[0],
        id: action.meta.dataset.id,
        fields: fields,
        loc: location }
      tables.push(table);
      return Object.assign({}, state, {
        metas: metas,
        tables: tables
      });
    case projectConstants.GET_META_CONNECTION:
      const linkData = [];
      for (let connection of action.connections){
        linkData.push({ from: connection.from_column_d.dataset.name.split('.')[0], fromPort: connection.from_column_d.column_name, to: connection.to_column_d.dataset.name.split('.')[0], toPort: connection.to_column_d.column_name });
      }
      return Object.assign({}, state, {
        connections: action.connections,
        linkData: linkData
      });
    case projectConstants.GET_DATASET_DATA_SUCCESS:
      let data= action.data;
      let keys=[];
      if(data.length>0)keys = Object.keys(data[0]);
      let arr = [];
      let columns = [];

      // for(let i=0;i<keys[0].length;i++){
      //     let dict ={};
      //     for(let key of keys){
      //       dict[key] = data[key][i];
      //     }
      //     arr.push(dict);
      // }
      for(let d of data) {
        arr.push(d)
      }

      for(let key of keys) {
        columns.push({
          Header: key,
          accessor: key
        });
      }

      return Object.assign({}, state, {
        dataset_data: arr,
        dataset_data_columns: columns
      });
    default:
      return state
  }

}

