import breezeway

bw = breezeway.BreezewayClient()

def test_breezeway_auth():
    assert bw.authenticated, 'Breezeway client should be authenticated'
    bw.company_id

def test_breezeway_company_api():
    assert bw.companies(), 'Companies list is should not be empty'
    assert bw.company_id, 'Company ID should not be None'
    templates = bw.templates()
    assert isinstance(templates, list), 'Template list should be a list'
    assert templates == bw.templates(company_id=bw.company_id), 'Templates should be the same when using company_id'

    # Breezeway return 200 with empty body when accessing unauthorized company templates
    # this seems like a bug in breezeway
    # with pytest.raises(BreezewayErrors.UnauthorizedError):
    #     bw.templates(company_id=bw.company_id + 1)

    subdepartments = bw.subdepartments()
    assert isinstance(subdepartments, list), 'Subdepartments list should be a list'

    # breezeway seems to completely ignore the queries when accessing subdepartments
    # this seems like a bug in breezeway
    # assert subdepartments == bw.subdepartments(company_id=bw.company_id), 'Subdepartments should be the same when using company_id'
    # with pytest.raises(BreezewayErrors.UnauthorizedError):
    #     bw.subdepartments(company_id=bw.company_id + 1)

def test_breezeway_people_api():
    active_users = bw.users()
    for user in active_users:
        assert isinstance(user.id, int), f'User ID should be an int, got {type(user.id)}'
        assert isinstance(user.first_name, str), f'First name should be a str, got {type(user.first_name)}'
        assert isinstance(user.last_name, str), f'Last name should be a str, got {type(user.last_name)}'
        assert isinstance(user.accept_decline_tasks, bool), f'Accept decline tasks should be a bool, got {type(user.accept_decline_tasks)}'
        assert isinstance(user.active, bool), f'Active should be a bool, got {type(user.active)}'
        assert user.active is True, f'Users from bw.users() should be active, user {user.id} has active status {user.active}'
        assert isinstance(user.emails, list), f'Emails should be a list, got {type(user.emails)}'
        for email in user.emails:
            assert isinstance(email, str), f'Email should be a str, got {type(email)}'
        assert isinstance(user.employee_code, str | None), f'Employee code should be str or None, got {type(user.employee_code)}'
        assert isinstance(user.groups, list), f'Groups should be a list, got {type(user.groups)}'
        for group in user.groups:
            assert isinstance(group, breezeway.UnitGroup), f'Group should be a UnitGroup, got {type(group)}'
        assert isinstance(user.type_departments, list), f'Departments should be a list, got {type(user.type_departments)}'
        for department in user.type_departments:
            assert isinstance(department, breezeway.Department), f'Department should be a Department, got {type(department)}'
        assert isinstance(user.type_role, breezeway.UserRole), f'Role should be a UserRole, got {type(user.type_role)}'
    invited_users = bw.users(status=breezeway.UserStatus.INVITED)
    for user in invited_users:
        if user.first_name.lower() == 'test':
            bw.invite(user.id)

def test_breezeway_unit_api():
    units = bw.units()
    for unit in units:
        assert isinstance(unit.id, int), f'Unit ID should be an int, got {type(unit.id)}'
        assert isinstance(unit.name, str), f'Unit name should be a str, got {type(unit.name)}'
        assert isinstance(unit.address1, str), f'Unit address1 should be a str, got {type(unit.address1)}'
        assert isinstance(unit.address2, str | None), f'Unit address2 should be a str or None, got {type(unit.address2)}'
        assert isinstance(unit.building, str | None), f'Unit building should be a str or None, got {type(unit.building)}'
        assert isinstance(unit.city, str), f'Unit city should be a str, got {type(unit.city)}'
        assert isinstance(unit.company_id, int), f'Unit company_id should be an int, got {type(unit.company_id)}'
        assert isinstance(unit.country, str), f'Unit country should be a str, got {type(unit.country)}'
        assert isinstance(unit.display, str), f'Unit display should be a str, got {type(unit.display)}'
        assert isinstance(unit.groups, list), f'Unit groups should be a list, got {type(unit.groups)}'
        for group in unit.groups:
            assert isinstance(group, breezeway.UnitGroup), f'Group should be a UnitGroup, got {type(group)}'
            assert isinstance(group.id, int), f'Group ID should be an int, got {type(group.id)}'
            assert isinstance(group.name, str), f'Group name should be a str, got {type(group.name)}'
            assert isinstance(group.parent_group_id, int | None), f'Group parent_group_id should be an int or None, got {type(group.parent_group_id)}'
        assert isinstance(unit.latitude, float | None), f'Unit latitude should be a float, got {type(unit.latitude)}'
        assert isinstance(unit.longitude, float | None), f'Unit longitude should be a float, got {type(unit.longitude)}'
        assert isinstance(unit.notes, breezeway.UnitNotes), f'Unit notes should be a UnitNotes, got {type(unit.notes)}'
        assert isinstance(unit.notes.access, str | None), f'Unit notes access should be a str or None, got {type(unit.notes.access)}'
        assert isinstance(unit.notes.general, str | None), f'Unit notes general should be a str or None, got {type(unit.notes.general)}'
        assert isinstance(unit.notes.wifi, str | None), f'Unit notes wifi should be a str or None, got {type(unit.notes.wifi)}'
        assert isinstance(unit.notes.about, str | None), f'Unit notes about should be a str or None, got {type(unit.notes.about)}'
        assert isinstance(unit.notes.direction, str | None), f'Unit notes direction should be a str or None, got {type(unit.notes.direction)}'