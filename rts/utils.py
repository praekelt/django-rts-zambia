from users.models import UserDistrict

class DistrictIdFilter:
    def __init__(self, parent=None, request=None, qs=None):
        self.request = request
        self.qs = qs
        self.parent = parent

    def queryset(self):
        if self.request.user.is_superuser:
            return self.qs
        elif UserDistrict.objects.filter(user_id=self.request.user.id).exists():
            emis_zone = ["SchoolDataAdmin", "HeadTeacherAdmin",
                         "TeacherPerformanceDataAdmin", "LearnerPerformanceDataAdmin"]
            created_by_emis = ["InboundSMSAdmin"]
            if self.parent.__class__.__name__ in emis_zone:
                return self.qs.filter(emis__zone__district=self.request.user.userdistrict.district_id)
            elif self.parent.__class__.__name__ in created_by_emis:
                return self.qs.filter(created_by__emis__zone__district=self.request.user.userdistrict.district_id)
            elif self.parent.__class__.__name__ == "SchoolAdmin":
                return self.qs.filter(zone__district=self.request.user.userdistrict.district_id)
        else:
            return self.qs


class ManagePermissions:
    def __init__(self, parent=None, request=None, actions=None, delete_perm=None):
        self.parent = parent
        self.request = request
        self.actions = actions
        self.delete_perm = delete_perm

    def remove_delete_permission(self):
        if not self.delete_perm:
            if 'delete_selected' in self.actions:
                del self.actions['delete_selected']
        return self.actions