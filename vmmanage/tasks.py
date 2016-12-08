from autotask.tasks import delayed_task
from uptomate import Deployment
from django.conf import settings
from .models import State, UNKNOWN_HOST
from subprocess import CalledProcessError
from time import sleep

MSG_SUCCESS = "Finished"
IN_USE_SLEEP_TIME = 10

@delayed_task(ttl=settings.TASK_TTL)
def run_on_vagr(vagr_depl, f, vm_db, callback=None, **kwargs):
    # TODO: Would be better to schedule the other tasks here
    # instead of waiting for the VM to get free
    # Wait until VM is free
    succeed = False
    while not succeed:
        succeed = vm_db.lock()
        sleep(IN_USE_SLEEP_TIME)

    if f != "status":
        try:
            getattr(Deployment.Vagrant, f)(vagr_depl, **kwargs)
        except BaseException:
            vm_db.unlock()
            raise
    if callback:
        callback(vagr_depl, f, vm_db, **kwargs)

    status = vagr_depl.status()
    vm_db.provider = status.provider
    vm_db.state_set.add(State(name=status.state), bulk=False)

    try:
        vm_db.ip_addr = vagr_depl.service_network_address()
    except CalledProcessError:
        # this does not work all the time, e.g. when the command
        # was 'stop', however, that should never affect the
        # result of the actual command called
        vm_db.ip_addr = UNKNOWN_HOST
    vm_db.unlock()
    return MSG_SUCCESS


@delayed_task(ttl=settings.TASK_TTL)
def status_of_deployment(vagr_depl):
    return vagr_depl.status().state


@delayed_task(ttl=settings.TASK_TTL)
def service_network_address(vagr_depl):
    return vagr_depl.service_network_address()


@delayed_task(ttl=settings.TASK_TTL)
def destroy_vm_db(vm):
    vm.delete()
    return MSG_SUCCESS


@delayed_task(ttl=settings.TASK_TTL)
def destroy_deployment(vagr_depl, vm):
    destroy_vm_db(vm)
    vagr_depl.destroy()
    return MSG_SUCCESS
