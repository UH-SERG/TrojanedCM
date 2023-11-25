hwaddr cpu_mips_translate_address(CPUMIPSState *env, target_ulong address, int rw)

{

    hwaddr physical;

    int prot;

    int access_type;

    int ret = 0;



    /* data access */

    access_type = ACCESS_INT;

    ret = get_physical_address(env, &physical, &prot,

                               address, rw, access_type);

    if (ret != TLBRET_MATCH) {

        raise_mmu_exception(env, address, rw, ret);

        return -1LL;

    } else {

        return physical;

    }

}
