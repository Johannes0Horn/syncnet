# coding=utf-8
def outer_factory():

    def inner_factory(ag__):

        def tf__contrastive_loss(Y, euclidean_distance):
            with ag__.FunctionScope('contrastive_loss', 'fscope', ag__.STD) as fscope:
                do_return = False
                retval_ = ag__.UndefinedReturnValue()
                margin = 1
                square_pred = ag__.converted_call(ag__.ld(K).square, (ag__.ld(euclidean_distance),), None, fscope)
                loss = ag__.converted_call(ag__.ld(K).mean, (((ag__.ld(Y) * (1 / ag__.ld(square_pred))) + ((1 - ag__.ld(Y)) * ag__.ld(square_pred))),), None, fscope)
                try:
                    do_return = True
                    retval_ = ag__.ld(loss)
                except:
                    do_return = False
                    raise
                return fscope.ret(retval_, do_return)
        return tf__contrastive_loss
    return inner_factory