# Python
from datetime import datetime
import random

# Django
from django.db.models.signals import post_save

# Project
from hierarchy.models import (Province, District, Zone, School)
from data.models import (HeadTeacher, SchoolData, TeacherPerformanceData,
                         SchoolMonitoringData,
                         LearnerPerformanceData, InboundSMS,
                         AcademicAchievementCode, DistrictAdminUser,
                         fire_ht_metric_if_new, fire_lp_metric_if_new,
                         fire_tp_metric_if_new, fire_sm_metric_if_new
                         )


NAMES = ['Aaliyah', 'Abayomi', 'Abebe', 'Abebi', 'Abena', 'Abeo', 'Ada']
SURNAMES = ['Azikiwe', 'Awolowo', 'Bello', 'Balewa', 'Akintola', 'Okotie-Eboh']
PROVINCE_NAMES = ['Central', 'Eastern', 'Lusaka', 'Muchinga', 'Northern', 'Southern', 'Western']
DISTRICT_NAMES = ['Chibombo', 'Kabwe', 'Kapiri Mposhi', 'Mkushi', 'Mumbwa']
ZONE_NAMES = ['zone_1', 'zone_1', 'zone_3', 'zone_4', 'zone_5', 'zone_6', 'zone_7', 'zone_8']
SCHOOL_NAMES = ['Baluba', 'Boyole', 'Buntungwa', 'Burma Road', 'Kansumbi', 'Mikomfwa', 'Zambezi']
ACHIEVEMENTS = ["highschool", "degree", "diploma", "masters"]
MESSAGES = ["Message 1", "Message 2", "Message 3"]


def random_name():
    return random.choice(NAMES)


def random_surname():
    return random.choice(SURNAMES)


def random_full_name():
    return '%s %s' % (random_name(), random_surname())


def random_province_name():
    return random.choice(PROVINCE_NAMES)


def random_district_name():
    return random.choice(DISTRICT_NAMES)


def random_zone_name():
    return random.choice(ZONE_NAMES)


def random_school_name():
    return random.choice(SCHOOL_NAMES)


def random_emis_value():
    return random.randint(1000, 9999)


def random_msisdn_value():
    return str(int(random.randint(1e10, 9e10)))


def random_achievement():
    return random.choice(ACHIEVEMENTS)


def random_message():
    return random.choice(MESSAGES)


def random_district():
    return create_district(random_district_name(), create_province("province"))


def random_datetime():
    year = random.randint(1960, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day)



def create_province(name=random_province_name()):
    province, _ = Province.objects.get_or_create(name=name)
    return province


def create_district(name=random_district_name(), province=None):
    if not province:
        province = create_province()

    district, _ = District.objects.get_or_create(province=province, name=name)
    return district


def create_zone(name=random_zone_name(), district=None):
    if not district:
        district = create_district()

    zone, _ = Zone.objects.get_or_create(district=district, name=name)
    return zone


def create_school(name=random_school_name(),
                  emis=random_emis_value(),
                  zone=None):
    if not zone:
        zone = create_zone()

    school, _ = School.objects.get_or_create(emis=emis, zone=zone, name=name)
    return school


def create_academic_level(achievement=random_achievement()):
    level, _ = AcademicAchievementCode.objects.get_or_create(achievement=achievement)
    return level


def create_headteacher(first_name=random_name(),
                       last_name=random_surname(),
                       msisdn=random_msisdn_value(),
                       date_of_birth=random_datetime().date(),
                       emis=None,
                       is_zonal_head=random.choice([True, False]),
                       gender=random.choice(["male", "female"])):

    if not emis:
        emis = create_school()

    data = {"first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "msisdn": msisdn,
            "date_of_birth": date_of_birth,
            "is_zonal_head": is_zonal_head,
            "emis": emis}
    headteacher, _ = HeadTeacher.objects.get_or_create(**data)
    return headteacher


def create_district_admin(first_name=random_name(),
                          last_name=random_surname(),
                          id_number=random_msisdn_value(),
                          date_of_birth=random_datetime().date(),
                          district=None):

    if not district:
        district = create_district()

    data = {"first_name": first_name,
            "last_name": last_name,
            "id_number": id_number,
            "date_of_birth": date_of_birth,
            "district": district}
    district_admin, _ = DistrictAdminUser.objects.get_or_create(**data)
    return district_admin

def create_school_data(emis=None,
                       name=random_name(),
                       classrooms=random.randint(1, 10),
                       teachers=random.randint(1, 10),
                       teachers_g1=random.randint(1, 10),
                       teachers_g2=random.randint(1, 10),
                       boys_g2=random.randint(1, 10),
                       girls_g2=random.randint(1, 10),
                       boys=random.randint(1, 10),
                       girls=random.randint(1, 10),
                       created_by=None):

    if not emis:
        emis = create_school()

    if not created_by:
        created_by = create_headteacher()

    data = {"emis": emis,
            "name": name,
            "classrooms": classrooms,
            "teachers": teachers,
            "teachers_g1": teachers_g1,
            "teachers_g2": teachers_g2,
            "boys_g2": boys_g2,
            "girls_g2": girls_g2,
            "boys": boys,
            "girls": girls,
            "created_by": created_by}

    schooldata, _ = SchoolData.objects.get_or_create(**data)
    return schooldata


def create_school_monitoring_data(see_lpip=random.choice(["yes", "yes_in_progress", "no"]),
                                   teaching=random.choice(["yes", "yes_in_progress", "no"]),
                                   learner_assessment=random.choice(["yes", "yes_in_progress", "no"]),
                                   learning_materials=random.choice(["yes", "yes_in_progress", "no"]),
                                   learner_attendance=random.choice(["yes", "yes_in_progress", "no"]),
                                   reading_time=random.choice(["yes", "yes_in_progress", "no"]),
                                   struggling_learners=random.choice(["yes", "yes_in_progress", "no"]),
                                   g2_observation_results=random.choice(["yes", "yes_in_progress", "no"]),
                                   ht_feedback=random.choice(["yes", "no"]),
                                   submitted_classroom=random.choice(["yes_cellphone", "yes_paper", "no"]),
                                   gala_sheets=random.choice(["yes", "yes_in_progress", "no"]),
                                   summary_worksheet=random.choice(["yes", "no"]),
                                   ht_feedback_literacy=random.choice(["yes", "no"]),
                                   submitted_gala=random.choice(["yes_cellphone", "yes_paper", "no"]),
                                   talking_wall=random.choice(["yes", "yes_not_updated", "no"]),
                                   emis=None,
                                   created_by=None):

    if not emis:
        emis = create_school()

    if not created_by:
        created_by = create_headteacher()

    data = {"see_lpip": see_lpip,
            "teaching": teaching,
            "learner_assessment": learner_assessment,
            "learning_materials": learning_materials,
            "learner_attendance": learner_attendance,
            "reading_time": reading_time,
            "struggling_learners": struggling_learners,
            "g2_observation_results": g2_observation_results,
            "ht_feedback": ht_feedback,
            "submitted_classroom": submitted_classroom,
            "gala_sheets": gala_sheets,
            "summary_worksheet": summary_worksheet,
            "ht_feedback_literacy": ht_feedback_literacy,
            "submitted_gala": submitted_gala,
            "talking_wall": talking_wall,
            "emis": emis,
            "created_by": created_by}

    school_mon, _ = SchoolMonitoringData.objects.get_or_create(**data)
    return school_mon


def create_teacher_perfomance_data(gender=random.choice(["male", "female"]),
                                   age=random.randint(20, 60),
                                   years_experience=random.randint(1, 60),
                                   g2_pupils_present=random.randint(20, 60),
                                   g2_pupils_registered=random.randint(20, 60),
                                   classroom_environment_score=random.randint(20, 60),
                                   t_l_materials=random.randint(20, 60),
                                   pupils_materials_score=random.randint(20, 60),
                                   pupils_books_number=random.randint(20, 60),
                                   reading_lesson=random.randint(20, 60),
                                   pupil_engagement_score=random.randint(20, 60),
                                   attitudes_and_beliefs=random.randint(20, 60),
                                   training_subtotal=random.randint(20, 60),
                                   ts_number=random.randint(20, 60),
                                   reading_assessment=random.randint(20, 60),
                                   reading_total=random.randint(20, 60),
                                   academic_level=None,
                                   emis=None,
                                   created_by=None):

    if not emis:
        emis = create_school()

    if not created_by:
        created_by = create_headteacher()

    if not academic_level:
        academic_level = create_academic_level()

    data = {"gender": gender,
            "age": age,
            "years_experience": years_experience,
            "g2_pupils_present": g2_pupils_present,
            "g2_pupils_registered": g2_pupils_registered,
            "classroom_environment_score": classroom_environment_score,
            "t_l_materials": t_l_materials,
            "pupils_materials_score": pupils_materials_score,
            "pupils_books_number": pupils_books_number,
            "reading_lesson": reading_lesson,
            "pupil_engagement_score": pupil_engagement_score,
            "attitudes_and_beliefs": attitudes_and_beliefs,
            "training_subtotal": training_subtotal,
            "ts_number": ts_number,
            "reading_assessment": reading_assessment,
            "reading_total": reading_total,
            "emis": emis,
            "academic_level": academic_level,
            "created_by": created_by}

    teacher_per, _ = TeacherPerformanceData.objects.get_or_create(**data)
    return teacher_per


def create_learner_perfomance_data(gender=random.choice(["male", "female"]),
                                   total_number_pupils=random.randint(1, 60),
                                   phonetic_awareness=random.randint(20, 60),
                                   vocabulary=random.randint(20, 60),
                                   reading_comprehension=random.randint(20, 60),
                                   writing_diction=random.randint(20, 60),
                                   below_minimum_results=random.randint(20, 60),
                                   minimum_results=random.randint(20, 60),
                                   desirable_results=random.randint(20, 60),
                                   outstanding_results=random.randint(20, 60),
                                   emis=None,
                                   created_by=None):
    if not emis:
        emis = create_school()

    if not created_by:
        created_by = create_headteacher()

    data = {"gender": gender,
            "total_number_pupils": total_number_pupils,
            "phonetic_awareness": phonetic_awareness,
            "vocabulary": vocabulary,
            "reading_comprehension": reading_comprehension,
            "writing_diction": writing_diction,
            "below_minimum_results": below_minimum_results,
            "minimum_results": minimum_results,
            "desirable_results": desirable_results,
            "outstanding_results": outstanding_results,
            "emis": emis,
            "created_by": created_by}

    learner_per, _ = LearnerPerformanceData.objects.get_or_create(**data)
    return learner_per


def create_inbound_sms(message=random_message(),
                       created_by=None):

    if not created_by:
        created_by = create_headteacher()

    data = {"message": message,
            "created_by": created_by}
    inbound_sms, _ = InboundSMS.objects.get_or_create(**data)
    return inbound_sms

""" Helpers for data app tests. """




class PostSaveHelper(object):
    """ Helper for managing post save hooks during tests. """

    def replace(self):
        """ Unhook post save hooks. """
        has_listeners = lambda: post_save.has_listeners(HeadTeacher)
        assert has_listeners(), (
            "HeadTeacher model has no post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")
        post_save.disconnect(fire_ht_metric_if_new, sender=HeadTeacher)
        assert not has_listeners(), (
            "HeadTeacher model still has post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")

        has_listeners = lambda: post_save.has_listeners(TeacherPerformanceData)
        assert has_listeners(), (
            "TeacherPerformanceData model has no post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")
        post_save.disconnect(fire_tp_metric_if_new, sender=TeacherPerformanceData)
        assert not has_listeners(), (
            "TeacherPerformanceData model still has post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")

        has_listeners = lambda: post_save.has_listeners(LearnerPerformanceData)
        assert has_listeners(), (
            "LearnerPerformanceData model has no post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")
        post_save.disconnect(fire_lp_metric_if_new, sender=LearnerPerformanceData)
        assert not has_listeners(), (
            "LearnerPerformanceData model still has post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")

        has_listeners = lambda: post_save.has_listeners(SchoolMonitoringData)
        assert has_listeners(), (
            "SchoolMonitoringData model has no post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")
        post_save.disconnect(fire_sm_metric_if_new, sender=SchoolMonitoringData)
        assert not has_listeners(), (
            "SchoolMonitoringData model still has post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")

    def restore(self):
        """ Restore post save hooks. """
        has_listeners = lambda: post_save.has_listeners(HeadTeacher)
        assert not has_listeners(), (
            "HeadTeacher model still has post_save listeners. Make sure"
            " helpers removed them properly in earlier tests.")
        post_save.connect(fire_ht_metric_if_new, sender=HeadTeacher)

        has_listeners = lambda: post_save.has_listeners(TeacherPerformanceData)
        assert not has_listeners(), (
            "TeacherPerformanceData model still has post_save listeners. Make sure"
            " helpers removed them properly in earlier tests.")
        post_save.connect(fire_tp_metric_if_new, sender=TeacherPerformanceData)

        has_listeners = lambda: post_save.has_listeners(LearnerPerformanceData)
        assert not has_listeners(), (
            "LearnerPerformanceData model still has post_save listeners. Make sure"
            " helpers removed them properly in earlier tests.")
        post_save.connect(fire_lp_metric_if_new, sender=LearnerPerformanceData)

        has_listeners = lambda: post_save.has_listeners(SchoolMonitoringData)
        assert not has_listeners(), (
            "SchoolMonitoringData model still has post_save listeners. Make sure"
            " helpers removed them properly in earlier tests.")
        post_save.connect(fire_sm_metric_if_new, sender=SchoolMonitoringData)


