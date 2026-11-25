// Lean compiler output
// Module: StronglyPolyLP
// Imports: public import Init public meta import Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
static lean_once_cell_t lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0;
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vadd(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vadd___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vsub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vsub___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vmul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vmul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_dot_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_dot_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_pathDiffSum(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_pathDiffSum___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_pathDiffSum_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_pathDiffSum_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* _init_lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(0u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot(lean_object* v_x_3_, lean_object* v_x_4_){
_start:
{
if (lean_obj_tag(v_x_3_) == 0)
{
goto v___jp_5_;
}
else
{
if (lean_obj_tag(v_x_4_) == 0)
{
goto v___jp_5_;
}
else
{
lean_object* v_head_7_; lean_object* v_tail_8_; lean_object* v_head_9_; lean_object* v_tail_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v_head_7_ = lean_ctor_get(v_x_3_, 0);
v_tail_8_ = lean_ctor_get(v_x_3_, 1);
v_head_9_ = lean_ctor_get(v_x_4_, 0);
v_tail_10_ = lean_ctor_get(v_x_4_, 1);
v___x_11_ = lean_int_mul(v_head_7_, v_head_9_);
v___x_12_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot(v_tail_8_, v_tail_10_);
v___x_13_ = lean_int_add(v___x_11_, v___x_12_);
lean_dec(v___x_12_);
lean_dec(v___x_11_);
return v___x_13_;
}
}
v___jp_5_:
{
lean_object* v___x_6_; 
v___x_6_ = lean_obj_once(&lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0, &lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0_once, _init_lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0);
return v___x_6_;
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___boxed(lean_object* v_x_14_, lean_object* v_x_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot(v_x_14_, v_x_15_);
lean_dec(v_x_15_);
lean_dec(v_x_14_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vadd(lean_object* v_x_17_, lean_object* v_x_18_){
_start:
{
if (lean_obj_tag(v_x_17_) == 0)
{
lean_dec(v_x_18_);
return v_x_17_;
}
else
{
if (lean_obj_tag(v_x_18_) == 0)
{
return v_x_18_;
}
else
{
lean_object* v_head_19_; lean_object* v_tail_20_; lean_object* v_head_21_; lean_object* v_tail_22_; lean_object* v___x_24_; uint8_t v_isShared_25_; uint8_t v_isSharedCheck_31_; 
v_head_19_ = lean_ctor_get(v_x_17_, 0);
v_tail_20_ = lean_ctor_get(v_x_17_, 1);
v_head_21_ = lean_ctor_get(v_x_18_, 0);
v_tail_22_ = lean_ctor_get(v_x_18_, 1);
v_isSharedCheck_31_ = !lean_is_exclusive(v_x_18_);
if (v_isSharedCheck_31_ == 0)
{
v___x_24_ = v_x_18_;
v_isShared_25_ = v_isSharedCheck_31_;
goto v_resetjp_23_;
}
else
{
lean_inc(v_tail_22_);
lean_inc(v_head_21_);
lean_dec(v_x_18_);
v___x_24_ = lean_box(0);
v_isShared_25_ = v_isSharedCheck_31_;
goto v_resetjp_23_;
}
v_resetjp_23_:
{
lean_object* v___x_26_; lean_object* v___x_27_; lean_object* v___x_29_; 
v___x_26_ = lean_int_add(v_head_19_, v_head_21_);
lean_dec(v_head_21_);
v___x_27_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vadd(v_tail_20_, v_tail_22_);
if (v_isShared_25_ == 0)
{
lean_ctor_set(v___x_24_, 1, v___x_27_);
lean_ctor_set(v___x_24_, 0, v___x_26_);
v___x_29_ = v___x_24_;
goto v_reusejp_28_;
}
else
{
lean_object* v_reuseFailAlloc_30_; 
v_reuseFailAlloc_30_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_30_, 0, v___x_26_);
lean_ctor_set(v_reuseFailAlloc_30_, 1, v___x_27_);
v___x_29_ = v_reuseFailAlloc_30_;
goto v_reusejp_28_;
}
v_reusejp_28_:
{
return v___x_29_;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vadd___boxed(lean_object* v_x_32_, lean_object* v_x_33_){
_start:
{
lean_object* v_res_34_; 
v_res_34_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vadd(v_x_32_, v_x_33_);
lean_dec(v_x_32_);
return v_res_34_;
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vsub(lean_object* v_x_35_, lean_object* v_x_36_){
_start:
{
if (lean_obj_tag(v_x_35_) == 0)
{
lean_dec(v_x_36_);
return v_x_35_;
}
else
{
if (lean_obj_tag(v_x_36_) == 0)
{
return v_x_36_;
}
else
{
lean_object* v_head_37_; lean_object* v_tail_38_; lean_object* v_head_39_; lean_object* v_tail_40_; lean_object* v___x_42_; uint8_t v_isShared_43_; uint8_t v_isSharedCheck_49_; 
v_head_37_ = lean_ctor_get(v_x_35_, 0);
v_tail_38_ = lean_ctor_get(v_x_35_, 1);
v_head_39_ = lean_ctor_get(v_x_36_, 0);
v_tail_40_ = lean_ctor_get(v_x_36_, 1);
v_isSharedCheck_49_ = !lean_is_exclusive(v_x_36_);
if (v_isSharedCheck_49_ == 0)
{
v___x_42_ = v_x_36_;
v_isShared_43_ = v_isSharedCheck_49_;
goto v_resetjp_41_;
}
else
{
lean_inc(v_tail_40_);
lean_inc(v_head_39_);
lean_dec(v_x_36_);
v___x_42_ = lean_box(0);
v_isShared_43_ = v_isSharedCheck_49_;
goto v_resetjp_41_;
}
v_resetjp_41_:
{
lean_object* v___x_44_; lean_object* v___x_45_; lean_object* v___x_47_; 
v___x_44_ = lean_int_sub(v_head_37_, v_head_39_);
lean_dec(v_head_39_);
v___x_45_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vsub(v_tail_38_, v_tail_40_);
if (v_isShared_43_ == 0)
{
lean_ctor_set(v___x_42_, 1, v___x_45_);
lean_ctor_set(v___x_42_, 0, v___x_44_);
v___x_47_ = v___x_42_;
goto v_reusejp_46_;
}
else
{
lean_object* v_reuseFailAlloc_48_; 
v_reuseFailAlloc_48_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_48_, 0, v___x_44_);
lean_ctor_set(v_reuseFailAlloc_48_, 1, v___x_45_);
v___x_47_ = v_reuseFailAlloc_48_;
goto v_reusejp_46_;
}
v_reusejp_46_:
{
return v___x_47_;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vsub___boxed(lean_object* v_x_50_, lean_object* v_x_51_){
_start:
{
lean_object* v_res_52_; 
v_res_52_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vsub(v_x_50_, v_x_51_);
lean_dec(v_x_50_);
return v_res_52_;
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vmul(lean_object* v_x_53_, lean_object* v_x_54_){
_start:
{
if (lean_obj_tag(v_x_53_) == 0)
{
lean_dec(v_x_54_);
return v_x_53_;
}
else
{
if (lean_obj_tag(v_x_54_) == 0)
{
return v_x_54_;
}
else
{
lean_object* v_head_55_; lean_object* v_tail_56_; lean_object* v_head_57_; lean_object* v_tail_58_; lean_object* v___x_60_; uint8_t v_isShared_61_; uint8_t v_isSharedCheck_67_; 
v_head_55_ = lean_ctor_get(v_x_53_, 0);
v_tail_56_ = lean_ctor_get(v_x_53_, 1);
v_head_57_ = lean_ctor_get(v_x_54_, 0);
v_tail_58_ = lean_ctor_get(v_x_54_, 1);
v_isSharedCheck_67_ = !lean_is_exclusive(v_x_54_);
if (v_isSharedCheck_67_ == 0)
{
v___x_60_ = v_x_54_;
v_isShared_61_ = v_isSharedCheck_67_;
goto v_resetjp_59_;
}
else
{
lean_inc(v_tail_58_);
lean_inc(v_head_57_);
lean_dec(v_x_54_);
v___x_60_ = lean_box(0);
v_isShared_61_ = v_isSharedCheck_67_;
goto v_resetjp_59_;
}
v_resetjp_59_:
{
lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_65_; 
v___x_62_ = lean_int_mul(v_head_55_, v_head_57_);
lean_dec(v_head_57_);
v___x_63_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vmul(v_tail_56_, v_tail_58_);
if (v_isShared_61_ == 0)
{
lean_ctor_set(v___x_60_, 1, v___x_63_);
lean_ctor_set(v___x_60_, 0, v___x_62_);
v___x_65_ = v___x_60_;
goto v_reusejp_64_;
}
else
{
lean_object* v_reuseFailAlloc_66_; 
v_reuseFailAlloc_66_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_66_, 0, v___x_62_);
lean_ctor_set(v_reuseFailAlloc_66_, 1, v___x_63_);
v___x_65_ = v_reuseFailAlloc_66_;
goto v_reusejp_64_;
}
v_reusejp_64_:
{
return v___x_65_;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vmul___boxed(lean_object* v_x_68_, lean_object* v_x_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_vmul(v_x_68_, v_x_69_);
lean_dec(v_x_68_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_dot_match__1_splitter___redArg(lean_object* v_x_71_, lean_object* v_x_72_, lean_object* v_h__1_73_, lean_object* v_h__2_74_, lean_object* v_h__3_75_){
_start:
{
if (lean_obj_tag(v_x_71_) == 0)
{
lean_object* v___x_76_; 
lean_dec(v_h__3_75_);
lean_dec(v_h__2_74_);
v___x_76_ = lean_apply_1(v_h__1_73_, v_x_72_);
return v___x_76_;
}
else
{
lean_dec(v_h__1_73_);
if (lean_obj_tag(v_x_72_) == 0)
{
lean_object* v___x_77_; 
lean_dec(v_h__3_75_);
v___x_77_ = lean_apply_2(v_h__2_74_, v_x_71_, lean_box(0));
return v___x_77_;
}
else
{
lean_object* v_head_78_; lean_object* v_tail_79_; lean_object* v_head_80_; lean_object* v_tail_81_; lean_object* v___x_82_; 
lean_dec(v_h__2_74_);
v_head_78_ = lean_ctor_get(v_x_71_, 0);
lean_inc(v_head_78_);
v_tail_79_ = lean_ctor_get(v_x_71_, 1);
lean_inc(v_tail_79_);
lean_dec_ref_known(v_x_71_, 2);
v_head_80_ = lean_ctor_get(v_x_72_, 0);
lean_inc(v_head_80_);
v_tail_81_ = lean_ctor_get(v_x_72_, 1);
lean_inc(v_tail_81_);
lean_dec_ref_known(v_x_72_, 2);
v___x_82_ = lean_apply_4(v_h__3_75_, v_head_78_, v_tail_79_, v_head_80_, v_tail_81_);
return v___x_82_;
}
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_dot_match__1_splitter(lean_object* v_motive_83_, lean_object* v_x_84_, lean_object* v_x_85_, lean_object* v_h__1_86_, lean_object* v_h__2_87_, lean_object* v_h__3_88_){
_start:
{
if (lean_obj_tag(v_x_84_) == 0)
{
lean_object* v___x_89_; 
lean_dec(v_h__3_88_);
lean_dec(v_h__2_87_);
v___x_89_ = lean_apply_1(v_h__1_86_, v_x_85_);
return v___x_89_;
}
else
{
lean_dec(v_h__1_86_);
if (lean_obj_tag(v_x_85_) == 0)
{
lean_object* v___x_90_; 
lean_dec(v_h__3_88_);
v___x_90_ = lean_apply_2(v_h__2_87_, v_x_84_, lean_box(0));
return v___x_90_;
}
else
{
lean_object* v_head_91_; lean_object* v_tail_92_; lean_object* v_head_93_; lean_object* v_tail_94_; lean_object* v___x_95_; 
lean_dec(v_h__2_87_);
v_head_91_ = lean_ctor_get(v_x_84_, 0);
lean_inc(v_head_91_);
v_tail_92_ = lean_ctor_get(v_x_84_, 1);
lean_inc(v_tail_92_);
lean_dec_ref_known(v_x_84_, 2);
v_head_93_ = lean_ctor_get(v_x_85_, 0);
lean_inc(v_head_93_);
v_tail_94_ = lean_ctor_get(v_x_85_, 1);
lean_inc(v_tail_94_);
lean_dec_ref_known(v_x_85_, 2);
v___x_95_ = lean_apply_4(v_h__3_88_, v_head_91_, v_tail_92_, v_head_93_, v_tail_94_);
return v___x_95_;
}
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_pathDiffSum(lean_object* v_x_96_, lean_object* v_x_97_){
_start:
{
if (lean_obj_tag(v_x_97_) == 0)
{
lean_object* v___x_98_; 
v___x_98_ = lean_obj_once(&lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0, &lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0_once, _init_lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_dot___closed__0);
return v___x_98_;
}
else
{
lean_object* v_head_99_; lean_object* v_tail_100_; lean_object* v___x_101_; lean_object* v___x_102_; lean_object* v___x_103_; 
v_head_99_ = lean_ctor_get(v_x_97_, 0);
v_tail_100_ = lean_ctor_get(v_x_97_, 1);
v___x_101_ = lean_int_sub(v_head_99_, v_x_96_);
v___x_102_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_pathDiffSum(v_head_99_, v_tail_100_);
v___x_103_ = lean_int_add(v___x_101_, v___x_102_);
lean_dec(v___x_102_);
lean_dec(v___x_101_);
return v___x_103_;
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_pathDiffSum___boxed(lean_object* v_x_104_, lean_object* v_x_105_){
_start:
{
lean_object* v_res_106_; 
v_res_106_ = lp_strongly_x2dpoly_x2dlp_StronglyPolyLP_pathDiffSum(v_x_104_, v_x_105_);
lean_dec(v_x_105_);
lean_dec(v_x_104_);
return v_res_106_;
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_pathDiffSum_match__1_splitter___redArg(lean_object* v_x_107_, lean_object* v_x_108_, lean_object* v_h__1_109_, lean_object* v_h__2_110_){
_start:
{
if (lean_obj_tag(v_x_108_) == 0)
{
lean_object* v___x_111_; 
lean_dec(v_h__2_110_);
v___x_111_ = lean_apply_1(v_h__1_109_, v_x_107_);
return v___x_111_;
}
else
{
lean_object* v_head_112_; lean_object* v_tail_113_; lean_object* v___x_114_; 
lean_dec(v_h__1_109_);
v_head_112_ = lean_ctor_get(v_x_108_, 0);
lean_inc(v_head_112_);
v_tail_113_ = lean_ctor_get(v_x_108_, 1);
lean_inc(v_tail_113_);
lean_dec_ref_known(v_x_108_, 2);
v___x_114_ = lean_apply_3(v_h__2_110_, v_x_107_, v_head_112_, v_tail_113_);
return v___x_114_;
}
}
}
LEAN_EXPORT lean_object* lp_strongly_x2dpoly_x2dlp___private_StronglyPolyLP_0__StronglyPolyLP_pathDiffSum_match__1_splitter(lean_object* v_motive_115_, lean_object* v_x_116_, lean_object* v_x_117_, lean_object* v_h__1_118_, lean_object* v_h__2_119_){
_start:
{
if (lean_obj_tag(v_x_117_) == 0)
{
lean_object* v___x_120_; 
lean_dec(v_h__2_119_);
v___x_120_ = lean_apply_1(v_h__1_118_, v_x_116_);
return v___x_120_;
}
else
{
lean_object* v_head_121_; lean_object* v_tail_122_; lean_object* v___x_123_; 
lean_dec(v_h__1_118_);
v_head_121_ = lean_ctor_get(v_x_117_, 0);
lean_inc(v_head_121_);
v_tail_122_ = lean_ctor_get(v_x_117_, 1);
lean_inc(v_tail_122_);
lean_dec_ref_known(v_x_117_, 2);
v___x_123_ = lean_apply_3(v_h__2_119_, v_x_116_, v_head_121_, v_tail_122_);
return v___x_123_;
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
void lean_initialize_runtime_module();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_strongly_x2dpoly_x2dlp_StronglyPolyLP(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize_runtime_module();
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
