from enum import Enum


class CyclePeriods(str, Enum):
    onetime = 'onetime'
    hour = 'hour'
    month = 'month'
    year = 'year'


class PublicStatuses(str, Enum):
    public = 'public'
    private = 'private'
    retired = 'retired'


class PricingModel(str, Enum):
    free = 'free'
    fixed_and_dynamic = 'fixed_and_dynamic'
    dynamic_or_fixed = 'dynamic_or_fixed'


class ProductAutoSetup(str, Enum):
    disabled = 'disabled'
    on_order = 'on_order'
    on_first_payment = 'on_first_payment'
    manual = 'manual'


class ProductType(str, Enum):
    generic = 'generic'
    openstack = 'openstack'
    hosting = 'hosting'
    domain = 'domain'
    cdn = 'cdn'


class ServiceStatus(str, Enum):
    pending = 'pending'
    active = 'active'
    suspended = 'suspended'
    terminated = 'terminated'
    canceled = 'canceled'
    fraud = 'fraud'
    archived = 'archived'


class OrderStatus(str, Enum):
    pending = 'pending'
    verified = 'verified'
    completed = 'completed'
    cancelled = 'cancelled'


class PaymentStatus(str, Enum):
    unpaid = 'unpaid'
    paid = 'paid'
    canceled = 'canceled'
    refunded = 'refunded'


class ServiceSuspendType(str, Enum):
    staff = 'staff'
    overdue = 'overdue'
    user_requested = 'userrequested'


class BillingItemTypes(str, Enum):
    service = 'service'
    credit = 'credit'
    setupfee = 'setupfee'
    other = 'other'


class ProvisioningBackend(str, Enum):
    openstack = "openstack"
    cdn = "cdn"
    database = "database"
    manual = "manual"
    external = "external"

class ConfigurableOptionWidget(str, Enum):
    dropdown = 'drop'
    yesno = 'yesno'
    radio = 'radio'
    number_input = 'num_in'
    text_input = 'text_in'

    @classmethod
    def with_choices(cls):
        return [cls.dropdown, cls.radio]

    @classmethod
    def without_choices(cls):
        return [cls.yesno, cls.number_input, cls.text_input]


class ConfigurableOptionStatus(str, Enum):
    public = 'public'
    private = 'private'
    retired = 'retired'
