import { projectConstants } from '../_constants';
import { userService } from '../_services';
import { alertActions, loaderActions } from './';
import { history } from '../_helpers';
var EventEmitter = require('events');

export const projectActions = {
    getTags,
    getDurations,
    addGroup,
    searchTag,
    allGroups,
    filterGroups,
    getGroupById,
    getMembersByGroupId,
    getChatsByGroupId,
    addChat,
    getGroupByUserId,
    getUsers,
    getJobTitles,
    addMember,
    addTags,
    promoteMember,
    deleteMember,
    getProjects,
    addProject,
    deleteProject,
    getProject,
    addDataset,
    deleteDataset,
    getDatasetMeta,
    clearState,
    getType,
    getRole,
    getImputation,
    updateMeta,
    addConnection,
    getConnections,
    deleteConnection,
    getDatasetData,
    getProblemType,
    createTraining,
    geTrainingDetail,
    geTrainingMetric,
    geTrainingModels,
    getAccuracy,
    getROC,
    getBluePrint,
    getFeatureImportance,
    getLossInteraction,
    getActualPrediction,
    mergeConnection,
    setDataset,
    getTimeType,
    deployModel,
    getDeployedModel,
    addTraining,
    getTestingSets,
    startTesting,
    getTestingGraph,
    getTaskProgress,
    filterTrainingModels,
    interruptTraining,
    updateLocation
};


function getTags() {
    return dispatch => {
        dispatch(request());

        userService.getTags()
            .then(
                tags => {
                    if(tags.success)
                        dispatch(success(tags.data));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.TAGS_REQUEST } }
    function success(tags) { return { type: projectConstants.TAGS_SUCCESS, tags } }
    function failure(error) { return { type: projectConstants.TAGS_FAILURE, error } }
}



function getProjects() {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getProjects()
            .then(
                project => {
                    if(project.success)
                        dispatch(success(project.results));
                        dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                    dispatch(loaderActions.requesting(false));
                }
            );
    };

    function success(projects) { return { type: projectConstants.GET_PROJECT_SUCCESS, projects } }
}

function getType() {
    return dispatch => {
        userService.getType()
            .then(
                type => {
                    if(type.success)
                        dispatch(success(type.results));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(meta_type) { return { type: projectConstants.GET_META_TYPE_SUCCESS, meta_type } }
}

function getProblemType() {
    return dispatch => {
        userService.getProblemType()
            .then(
                type => {
                    if(type.success)
                        dispatch(success(type.results));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(problem_type) { return { type: projectConstants.GET_PROBLEM_TYPE_SUCCESS, problem_type } }
}

function getTimeType() {
    return dispatch => {
        userService.getTimeType()
            .then(
                type => {
                    if(type.success)
                        dispatch(success(type.results));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(time_type) { return { type: projectConstants.GET_TIME_TYPE_SUCCESS, time_type } }
}



function getRole() {
    return dispatch => {
        userService.getRole()
            .then(
                role => {
                    if(role.success)
                        dispatch(success(role.results));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(meta_role) { return { type: projectConstants.GET_META_ROLE_SUCCESS, meta_role } }
}

function getImputation() {
    return dispatch => {
        userService.getImputation()
            .then(
                imputation => {
                    if(imputation.success)
                        dispatch(success(imputation.results));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(meta_imputation) { return { type: projectConstants.GET_META_IMPUTATION_SUCCESS, meta_imputation } }
}


function getDatasetMeta(dataset) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getMeta(dataset.id)
            .then(
                meta => {
                    if(meta.success){
                        dispatch(success({dataset: dataset, meta: meta.data}));
                    }
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                    dispatch(loaderActions.requesting(false));
                }
            );
    };
    function success(meta) { return { type: projectConstants.GET_META_SUCCESS, meta } }
}

function clearState() {
    return { type: projectConstants.CLEAR_META_STATE }
}

function setDataset(selected_dataset, selected_metas) {
    return { type: projectConstants.SET_SELECTED_SUCCESS, selected_dataset, selected_metas }
}

function addProject(project) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.addProject(project)
            .then(
                project => {
                    if(project.success)
                        dispatch(alertActions.success('Project creation successful'));
                    dispatch(loaderActions.requesting(false));
                    dispatch(getProjects());
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function createTraining(detail, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.createTraining(detail)
            .then(
                detail => {
                    if(detail.success){
                        // dispatch(alertActions.success('Training started successfully.'));
                        history.push('/training/'+project_id);
                    }
                    dispatch(loaderActions.requesting(false));

                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}



function updateMeta(id, request) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));
        userService.updateMeta(id, request)
            .then(
                project => {
                    if(project.success)
                        dispatch(alertActions.success('Meta updated successfully.'));
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}


function updateLocation(nodes) {
    return dispatch => {
        userService.updateLoc(nodes)
            .then(
                resp => {
                    console.log('update loc', resp);
                },
                error => {
                    console.log('error loc', error);
                }
            );
    };
}


function addConnection(project_id, request) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));
        userService.addConnection(request)
            .then(
                connection => {
                    if(connection.success)
                        dispatch(alertActions.success('Meta connection added successfully.'));
                    dispatch(loaderActions.requesting(false));
                    dispatch(getConnections(project_id));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}


function deleteConnection(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));
        userService.deleteConnection(id)
            .then(
                connection => {
                    if(connection.success)
                        dispatch(alertActions.success('Meta connection deleted successfully.'));
                    dispatch(loaderActions.requesting(false));
                    dispatch(getConnections(project_id));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function mergeConnection(project_id, request) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));
        userService.mergeConnections(project_id, request)
            .then(
                connection => {
                    if(connection.success)
                        dispatch(alertActions.success('Meta connections processed successfully.'));
                    dispatch(loaderActions.requesting(false));
                    dispatch(getConnections(project_id));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function deployModel(detail, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.deployModel(detail)
            .then(
                resp => {
                    console.log('in resp here', resp);
                    if(resp.success){
                        setTimeout(()=>{
                            dispatch(alertActions.success('Model deployed successfully.'));
                        },1000);
                        history.push('/graph/'+project_id);
                    }
                    dispatch(loaderActions.requesting(false));

                },
                error => {
                    console.log('in error here', error);
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function getDeployedModel(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getDeployedModel(id)
            .then(
                model => {
                    if(model.success)
                        dispatch(success(model.data));
                        if(model.data.length > 0){
                            let model_d = model.data[0].model_d;
                            if(model_d.training.processed_file_d.parent == undefined){
                                dispatch(projectActions.getTestingSets(model_d.training.processed_file))
                            }
                            else{
                                for(let i of model_d.training.processed_file_d.parent.dataset){
                                    dispatch(projectActions.getTestingSets(i))
                                }
                            }
                        }
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(model) { return { type: projectConstants.GET_DEPLOYED_MODEL, model } }
}

function getTestingSets(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getTestingData(id)
            .then(
                training => {
                    if(training.success)
                        dispatch(success(training.data));
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(testing) { return { type: projectConstants.GET_TESTING_SET, testing } }
}


function getTestingGraph(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getTestingGraph(id)
            .then(
                graph => {
                    if(graph.success)
                        dispatch(success(graph.data));
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(graph) { return { type: projectConstants.GET_TESTING_GRAPH, graph } }
}

function startTesting(id, project) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.startTesting(id, project)
            .then(
                training => {
                    if(training.success)
                        dispatch(alertActions.success('Testing started successful'));
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}


function getConnections(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getMetaConnections(id)
            .then(
                connections => {
                    if(connections.success)
                        dispatch(success(connections.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(connections) { return { type: projectConstants.GET_META_CONNECTION, connections } }
}


function getTaskProgress(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getTaskProgress(id)
            .then(
                task => {
                    if(task.success)
                        dispatch(success(task.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    // dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(task) { return { type: projectConstants.GET_TASK_PROGRESS, task } }
}


function getDatasetData(id, offset=0) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getDatasetData(id, offset)
            .then(
                data => {
                    if(data.success)
                        dispatch(success(data.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(data) { return { type: projectConstants.GET_DATASET_DATA_SUCCESS, data } }
}


function deleteProject(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.deleteProject(id)
            .then(
                project => {
                    if(project.success)
                        dispatch(alertActions.success('Project deletion successful'));
                    dispatch(loaderActions.requesting(false));
                    dispatch(getProjects());
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function deleteDataset(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.deleteDataset(id)
            .then(
                project => {
                    if(project.success)
                        dispatch(alertActions.success('Dataset deletion successful'));
                    dispatch(loaderActions.requesting(false));
                    dispatch(getProject(project_id));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function getProject(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getProject(id)
            .then(
                project => {
                    if(project.success)
                        dispatch(success(project.result))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(project) { return { type: projectConstants.GET_ONE_PROJECT_SUCCESS, project } }
}


function geTrainingDetail(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getTrainingDetail(id)
            .then(
                training => {
                    if(training.success)
                        dispatch(success(training.data));
                        if(training.data.length > 0)
                            dispatch(projectActions.geTrainingModels(training.data[0].id));
                        else
                            history.push('/dashboard/'+id);

                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(training) { return { type: projectConstants.GET_TRAINING_DETAIL_SUCCESS, training } }
}

function geTrainingModels(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getTrainingModels(id)
            .then(
                models => {
                    if(models.success)
                        dispatch(success(models.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(models) { return { type: projectConstants.GET_TRAINING_MODELS_SUCCESS, models } }
}


function filterTrainingModels(id, metric) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.filterTrainingModels(id, metric)
            .then(
                models => {
                    if(models.success)
                        dispatch(success(models.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(models) { return { type: projectConstants.GET_TRAINING_MODELS_SUCCESS, models } }
}

function getAccuracy(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getAccuracy(id, project_id)
            .then(
                resp => {
                    dispatch(success(resp.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(resp) { return { type: projectConstants.GET_ACCURACY_SUCCESS, resp } }
}


function getROC(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getROC(id, project_id)
            .then(
                resp => {
                    dispatch(success(resp.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(resp) { return { type: projectConstants.GET_ROC_SUCCESS, resp } }
}


function getBluePrint(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getBluePrint(id, project_id)
            .then(
                resp => {
                    dispatch(success(resp.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(resp) { return { type: projectConstants.GET_BLUE_PRINT_SUCCESS, resp } }
}


function getFeatureImportance(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getFeatureImportance(id, project_id)
            .then(
                resp => {
                    dispatch(success(resp.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(resp) { return { type: projectConstants.GET_FEATURE_IMPORTANCE_SUCCESS, resp } }
}


function getLossInteraction(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getLossInteraction(id, project_id)
            .then(
                resp => {
                    dispatch(success(resp.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(resp) { return { type: projectConstants.GET_LOSS_INTERACTION_SUCCESS, resp } }
}


function getActualPrediction(id, project_id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.getActualPrediction(id, project_id)
            .then(
                resp => {
                    dispatch(success(resp.data))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(resp) { return { type: projectConstants.GET_ACTUAL_PREDICTION_SUCCESS, resp } }
}


function geTrainingMetric() {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));
        userService.getTrainingMetric()
            .then(
                metric => {
                    if(metric.success)
                        dispatch(success(metric.results))
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(metric) { return { type: projectConstants.GET_TRAINING_METRIC_SUCCESS, metric } }
}



function addDataset(request, id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.addDataset(request, progressCallback)
            .then(
                project => {
                    if(project.success)
                        dispatch(alertActions.success('Dataset task added successfully'));
                    dispatch(loaderActions.requesting(false));
                    // dispatch(getProject(id));
                },
                error => {
                    var ee = new EventEmitter();
                    ee.emit('error', 'failed!');
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function progressCallback(progress) {
        return dispatch => {
            console.log('progress here', progress);
            dispatch(success(progress.loaded / progress.total * 100));
        }
        function success(progress) {
            return {type: projectConstants.GET_PROGRESS_SUCCESS, progress}
        };
    }
}

function addTraining(request, id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.addTesting(request)
            .then(
                project => {
                    if(project.success)
                        dispatch(alertActions.success('Testing data uploaded successfully'));
                    dispatch(loaderActions.requesting(false));
                    // dispatch(getProject(id));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function interruptTraining(id) {
    return dispatch => {
        dispatch(loaderActions.requesting(true, true));

        userService.interruptTraining(id)
            .then(
                project => {
                    if(project.success)
                        dispatch(alertActions.success('Interruption in progress.'));
                    dispatch(getProject(id));
                    dispatch(loaderActions.requesting(false));
                },
                error => {
                    dispatch(loaderActions.requesting(false));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
}

function getUsers() {
    return dispatch => {
        userService.getUsers()
            .then(
                users => {
                    if(users.success)
                        dispatch(success(users.results));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function success(users) { return { type: projectConstants.GET_ALL_USERS_SUCCESS, users } }
}

function getJobTitles() {
    return dispatch => {
        userService.getJobTitles()
            .then(
                titles => {
                    if(titles.success)
                        dispatch(success(titles.results));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function success(titles) { return { type: projectConstants.GET_ALL_JOBTITLES_SUCCESS, titles } }
}





function getDurations() {
    return dispatch => {
        dispatch(request());

        userService.getDurations()
            .then(
                durations => {
                    if(durations.success)
                        dispatch(success(durations.results));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.DURATION_REQUEST } }
    function success(durations) { return { type: projectConstants.DURATION_SUCCESS, durations } }
    function failure(error) { return { type: projectConstants.DURATON_FAILURE, error } }
}

function searchTag(value) {
    return dispatch => {
        dispatch(request());

        userService.searchTag(value)
            .then(
                tags => {
                    if(tags.success)
                        dispatch(success(tags.data));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function request() { return { type: projectConstants.SEARCH_TAG_REQUEST } }
    function success(tags) { return { type: projectConstants.SEARCH_TAG_SUCCESS, tags } }
    function failure(error) { return { type: projectConstants.SEARCH_TAG_FAILURE, error } }
}


function addGroup(group) {
    return dispatch => {
        dispatch(request());

        userService.addGroup(group)
            .then(
                group => {
                    if(group.success)
                        // dispatch(success(true));
                        history.push('/');
                        dispatch(alertActions.success('Group creation successful'));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.ADD_GROUP_REQUEST } }
    function success(created) { return { type: projectConstants.ADD_GROUP_SUCCESS, created } }
    function failure(error) { return { type: projectConstants.ADD_GROUP_FAILURE, error } }
}


function addChat(chat, group_id) {
    return dispatch => {
        dispatch(request());

        userService.addChat(chat)
            .then(
                chat => {
                    if(chat.success)
                        // dispatch(success(true));
                        dispatch(alertActions.success('Message creation successful'));
                        dispatch(getChatsByGroupId(group_id));
                        dispatch(success(true));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function request() { return { type: projectConstants.ADD_CHAT_REQUEST } }
    function success(created) { return { type: projectConstants.ADD_GROUP_SUCCESS, created } }
    function failure(error) { return { type: projectConstants.ADD_GROUP_FAILURE, error } }
}


function addMember(member, group_id) {
    return dispatch => {

        userService.addMemeber(member)
            .then(
                chat => {
                    if(chat.success)
                        // dispatch(success(true));
                        dispatch(alertActions.success('Member creation successful'));
                        dispatch(getMembersByGroupId(group_id));
                        dispatch(success(true));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(created) { return { type: projectConstants.GET_ADD_MEMBER_SUCCESS, created } }
}

function promoteMember(member, group_id) {
    return dispatch => {

        userService.promoteMember(member)
            .then(
                m => {
                    if(m.success)
                        // dispatch(success(true));
                        dispatch(alertActions.success('Member creation successful'));
                        dispatch(getMembersByGroupId(group_id));
                        dispatch(success(true));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(updated) { return { type: projectConstants.PROMOTE_MEMBER_SUCCESS, updated } }
}

function deleteMember(member, group_id) {
    return dispatch => {

        userService.deleteMember(member)
            .then(
                m => {
                    if(m.success)
                        // dispatch(success(true));
                        dispatch(alertActions.success('Member deletion successful'));
                        dispatch(getMembersByGroupId(group_id));
                        dispatch(success(true));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(deleted) { return { type: projectConstants.DELETE_MEMBER_SUCCESS, deleted } }
}


function addTags(tag) {
    return dispatch => {

        userService.addTag(tag)
            .then(
                chat => {
                    if(chat.success)
                        // dispatch(success(true));
                        dispatch(alertActions.success('Tag creation successful'));
                        dispatch(getTags());
                        dispatch(success(true));
                },
                error => {
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };
    function success(created) { return { type: projectConstants.GET_ADD_TAG_SUCCESS, created } }
}


function allGroups() {
    return dispatch => {
        dispatch(request());

        userService.allGroups()
            .then(
                group => {
                    if(group.success)
                        dispatch(success(group.results));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.FILTER_GROUP_REQUEST } }
    function success(groups) { return { type: projectConstants.FILTER_GROUP_SUCCESS, groups } }
    function failure(error) { return { type: projectConstants.FILTER_GROUP_FAILURE, error } }
}


function filterGroups(tags) {
    return dispatch => {
        dispatch(request());

        userService.filterGroups(tags)
            .then(
                group => {
                    if(group.success)
                        dispatch(success(group.data));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.FILTER_GROUP_REQUEST } }
    function success(groups) { return { type: projectConstants.FILTER_GROUP_SUCCESS, groups } }
    function failure(error) { return { type: projectConstants.FILTER_GROUP_FAILURE, error } }
}


function getGroupById(id) {
    return dispatch => {
        dispatch(request());

        userService.getGroupById(id)
            .then(
                group => {
                    if(group.success)
                        dispatch(success(group.result));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.GET_GROUP_REQUEST } }
    function success(groups) { return { type: projectConstants.GET_GROUP_SUCCESS, groups } }
    function failure(error) { return { type: projectConstants.GET_GROUP_FAILURE, error } }
}


function getGroupByUserId(id) {
    return dispatch => {
        dispatch(request());

        userService.getGroupByUserId(id)
            .then(
                groups => {
                    if(groups.success)
                        dispatch(success(groups.data));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.GET_GROUP_BY_USER_REQUEST } }
    function success(groups) { return { type: projectConstants.GET_GROUP_BY_USER_SUCCESS, groups } }
    function failure(error) { return { type: projectConstants.GET_GROUP_BY_USER_FAILURE, error } }
}


function getMembersByGroupId(id) {
    return dispatch => {
        dispatch(request());

        userService.getMembersGroupById(id)
            .then(
                group => {
                    if(group.success)
                        dispatch(success(group.data));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.GET_GROUP_MEMBERS_REQUEST } }
    function success(members) { return { type: projectConstants.GET_GROUP_MEMBERS_SUCCESS, members } }
    function failure(error) { return { type: projectConstants.GET_GROUP_MEMBERS_FAILURE, error } }
}


function getChatsByGroupId(id) {
    return dispatch => {
        dispatch(request());

        userService.getChatsGroupById(id)
            .then(
                chats => {
                    if(chats.success)
                        dispatch(success(chats.data));
                },
                error => {
                    dispatch(failure(error.toString()));
                    dispatch(alertActions.error(error.toString()));
                }
            );
    };

    function request() { return { type: projectConstants.GET_GROUP_CHAT_REQUEST } }
    function success(chats) { return { type: projectConstants.GET_GROUP_CHAT_SUCCESS, chats } }
    function failure(error) { return { type: projectConstants.GET_GROUP_CHAT_FAILURE, error } }
}