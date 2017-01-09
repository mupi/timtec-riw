(function(angular){

    angular.module('users-admin.controllers', []).
        controller('UsersAdminController', ['$scope', '$window', '$modal', '$http', '$q',  'UserAdmin',
        function($scope, $window, $modal, $http, $q, UserAdmin) {

            var success_save_msg = 'Alterações salvas com sucesso.';
            var error_save_msg = 'Não foi possível salvar as alterações.';

            var confirm_delete_user_msg = 'Tem certeza que deseja apagar este usuário? Esta operação não poderá ser desfeita!';
            var success_delete_user_msg = 'Usuário apagado com sucesso.';
            var error_delete_user_msg = 'Erro ao apagar usuário.';

            $scope.total_users_found = parseInt($window.total_users_found, 10);

            $scope.users_page = UserAdmin.query({page: 1});

            $scope.filters = {};

            $scope.filter_users = function() {
                $scope.users_page = UserAdmin.query($scope.filters, function(users_page) {
                    $scope.filtered = true;
                    $scope.total_users_found = users_page.length;
                });
            };

            $scope.page_changed = function() {
                $scope.users_page = UserAdmin.query({page: $scope.current_page});
            };

            $scope.update_user = function(user) {
                user.$update({user_id: user.id}, function() {
                    $scope.alert.success(success_save_msg);
                }, function() {
                    $scope.alert.error(error_save_msg);
                });
            };

            //$scope.change_blocked_user_status = function(user) {
            //    user.$update({user_id: user.id}, function() {
            //        $scope.alert.success(success_save_msg);
            //    }, function() {
            //        $scope.alert.error(error_save_msg);
            //    });
            //};

            $scope.delete_user = function(user, index) {
                if (confirm(confirm_delete_user_msg)) {
                    user.$remove({user_id: user.id}, function() {
                        $scope.users_page.splice(index, 1);
                        $scope.alert.success(success_delete_user_msg);
                    }, function() {
                        $scope.alert.error(error_delete_user_msg);
                    });
                }
            };

            //
            //$scope.permissions_changed = false;
            //
            //$window.onbeforeunload = function (e) {
            //    if ($scope.permissions_changed) {
            //        if (!confirm('Você ainda não salvou suas alterações, tem certeza que deseja sair desta página?')) {
            //            event.preventDefault();
            //        }
            //    }
            //};
            //
            //$scope.courseId = /course\/([^\/]+)\/permissions/.extract(location.pathname, 1);
            //$scope.professors = CourseProfessor.query({course: $scope.courseId, has_user: true}, function(professors){
            //    $scope.professors_before_changes = angular.copy(professors);
            //});
            //
            //$scope.save_permissions = function() {
            //    var promises_list = [];
            //    //var new_course_professor;
            //    $scope.professors.forEach(function(course_professor) {
            //        if (course_professor.id){
            //            course_professor.$update({id: course_professor.id});
            //            promises_list.push(course_professor.$promise);
            //        } else {
            //            course_professor = course_professor.$save({
            //                course: course_professor.course,
            //                user: course_professor.user
            //            });
            //            promises_list.push(course_professor.$promise);
            //        }
            //    });
            //    $q.all([promises_list]).then(function(results) {
            //            $scope.alert.success(success_save_msg);
            //            $scope.permissions_changed = false;
            //        }, function(errorMsg) {
            //            $scope.alert.error(error_save_msg);
            //        }
            //    );
            //};
            //
            //$scope.cancel_permissions_changes = function() {
            //    $scope.professors = $scope.professors_before_changes;
            //    $scope.permissions_changed = false;
            //    $scope.alert.success(cancel_changes_msg);
            //};
            //
            //$scope.remove_professor = function(course_professor_id, index) {
            //    if(!confirm('Tem certeza que deseja remover este professor deste curso?')) return;
            //    if (course_professor_id)
            //        CourseProfessor.remove({id: course_professor_id});
            //    $scope.professors.splice(index, 1);
            //    $scope.permissions_changed = true;
            //};
            //
            //$scope.update_professor_role = function(professor) {
            //    $scope.permissions_changed = true;
            //};
            //
            //$scope.new_professors = function () {
            //    var modalInstance = $modal.open({
            //        templateUrl: 'newProfessorModal.html',
            //        controller: ['$scope', '$modalInstance', 'course_id', addProfessorsModalInstanceCtrl],
            //        resolve: {
            //            course_id: function () {
            //                return $scope.course_id;
            //            }
            //        }
            //    });
            //    modalInstance.result.then(function (new_professors) {
            //        angular.forEach(new_professors, function(professor){
            //            var new_professor = new CourseProfessor();
            //            new_professor.course =  $scope.courseId;
            //            new_professor.user = professor.id;
            //            new_professor.user_info = professor;
            //            $scope.professors.unshift(new_professor);
            //            $scope.permissions_changed = true;
            //        });
            //    });
            //};
            //var addProfessorsModalInstanceCtrl = function ($scope, $modalInstance, course_id) {
            //
            //    $scope.new_professors = [];
            //    $scope.add_professors = function () {
            //        $modalInstance.close($scope.new_professors);
            //    };
            //
            //    $scope.cancel = function () {
            //        $modalInstance.dismiss();
            //    };
            //
            //    $scope.on_select_professor = function(model) {
            //        $scope.new_professors.unshift(model);
            //        $scope.asyncSelected = '';
            //    };
            //
            //    $scope.remove_new_professor = function(index) {
            //        $scope.new_professors.splice(index, 1);
            //    };
            //
            //    $scope.getUsers = function(val) {
            //        return $http.get('/api/user_search', {
            //            params: {
            //              name: val,
            //              sensor: false
            //            }
            //        }).then(function(res){
            //            var professors_found = [];
            //            angular.forEach(res.data, function(item){
            //                var formated_name = '';
            //                if (item.first_name)
            //                    formated_name += item.first_name;
            //                if (item.last_name)
            //                    formated_name = formated_name + ' ' + item.last_name;
            //                if (formated_name)
            //                    formated_name = formated_name + ' - ';
            //                formated_name += item.username;
            //                if (item.email)
            //                    formated_name = formated_name + ' - ' + item.email;
            //                item.formated_name = formated_name;
            //                professors_found.push(item);
            //            });
            //            return professors_found;
            //        });
            //    };
            //};
        }
    ]);

})(angular);
