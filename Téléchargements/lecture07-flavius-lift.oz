% LINFO1131

% Lecture 8 (Nov. 22, 2023)

% Message-passing concurrency and multi-agent programming

% - Port objects and active objects
% - Flavius Josephus problem: comparing active objects and deterministic dataflow
% - Lift control system: example of a realistic multi-agent system

%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%

% 1. Port objects and active objects

% 1.1. Port object with internal state
declare
fun {NewPortObject Init Fun}
   P
in
   thread Sin Sout in
      {NewPort Sin P}
      {FoldL Sin Fun Init Sout}
   end
   P
end

% 1.2. Port object without internal state
declare
fun {NewPortObject2 Proc}
   P
in
   thread Sin in
      {NewPort Sin P}
      for Msg in Sin do {Proc Msg} end
   end
   P
end

% 1.3. Active object (port object with a class)
declare
fun {NewActive Class Init}
   Obj={New Class Init}
   P
in
   thread S in
      {NewPort S P}
      for M in S do {Obj M} end
   end
   proc {$ M} {Send P M} end
end


%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%

% 2. Flavius Josephus problem

% We define two versions of this problem:
% - Active object version with a class definition
% - Deterministic dataflow version with streams
% We can make a dataflow version because the
% Flavius Josephus problem is deterministic.
% Compare the two!  Which is longest, which is shortest!

% 2.1 Active object version of Flavius Josephus
declare
class Victim
   attr ident alive step last succ
   meth init(I K L)
      alive:=true step:=K last:=L ident:=I
   end
   meth setSucc(S) succ:=S end
   meth kill(X S)
      if @alive then
	 if S==1 then
	    @last=@ident
	 elseif X mod @step ==0 then
	    alive:=false
	    {@succ kill(X+1 S-1)}
	 else
	    {@succ kill(X+1 S)}
	 end
      else
	 {@succ kill(X S)}
      end
   end
end

declare
fun {Josephus N K}
   A={NewArray 1 N null}
   Last
in
   % N objects
   for I in 1..N do
      A.I:={NewActive Victim init(I K Last)}
   end
   % Connect them into a ring
   for I in 1..(N-1) do
      {A.I setSucc(A.(I+1))}
   end
   {A.N setSucc(A.1)}
   {A.1 kill(1 N)}
   Last
end

{Browse {Josephus 5 2}}

{Browse {Josephus 40 3}}

{Browse {Josephus 1000 100}}

%%%%%%%%%%%%%%%%%%%

% 2.2 Optimized active object version that removes dead victims from ring
% Also known as "short-circuit" version

declare
class Victim2
   attr ident alive step last succ pred
   meth init(I K L)
      alive:=true step:=K last:=L ident:=I
   end
   meth setSucc(S) succ:=S end
   meth setPred(P) pred:=P end
   meth kill(X S)
      if @alive then
	 if S==1 then
	    @last=@ident
	 elseif X mod @step ==0 then
	    alive:=false
	    {@pred setSucc(@succ)} % The order of these messages is critical
	    {@succ setPred(@pred)} % Kill message must encounter a correct ring
	    {@succ kill(X+1 S-1)}  % This works because of FIFO message property
	 else
	    {@succ kill(X+1 S)}
	 end
      else
	 {@succ kill(X S)}
      end
   end
end

declare
fun {Josephus2 N K}
   A={NewArray 1 N null}
   Last
in
   % N objects
   for I in 1..N do
      A.I:={NewActive Victim2 init(I K Last)}
   end
   % Connect them into a ring
   for I in 1..(N-1) do
      {A.I setSucc(A.(I+1))}
   end
   {A.N setSucc(A.1)}
   % Correctly set the predecessors
   for I in 2..N do
      {A.I setPred(A.(I-1))}
   end
   {A.1 setPred(A.N)}
   {A.1 kill(1 N)}
   Last
end

{Browse {Josephus2 5 2}}
{Browse {Josephus2 1000 100}}

%%%%%%%%%%%%%%%%%%%

% 2.3 Deterministic dataflow version of Flavius Josephus
% Code is very compact: streams are compacter than explicit message passing
% This is only possible because Flavius Josephus is a deterministic algorithm
% This version does the short-circuit optimization

% Exercise: try to make each line of versions 2.2 and 2.3 correspond.

declare
fun {Pipe Xs L H F}
   if L>H then Xs else {Pipe {F Xs L} L+1 H F} end
end

declare
fun {Josephus3 N K}
   fun {Victim Xs I}
      case Xs of kill(X S)|Xr then
	 if S==1 then Last=I nil
	 elseif X mod K == 0 then
	    kill(X+1 S-1)|Xr
	 else
	    kill(X+1 S)|{Victim Xr I}
	 end
      [] nil then nil end
   end
   Last Zs
in
   Zs={Pipe kill(1 N)|Zs 1 N
       fun {$ Is I} thread {Victim Is I} end end}
   Last
end

{Browse {Josephus3 5 2}}
{Browse {Josephus3 40 3}}
{Browse {Josephus3 1000 100}}

%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%

% 3. Lift control system

% This is an example of a realistic multi-agent system.

% Each kind of port object is first defined by drawing a complete state diagram.
% Then the state diagram is translated into code.  The hard part is defining the
% state diagram.  Translating into code is easy!  The code has two nested case
% statements, one case statement for the current state and a second case for the
% message that arrives.  The result is the new state.

% 1.1. Port object with internal state
declare
fun {NewPortObject Init Fun}
   P
in
   thread Sin Sout in
      {NewPort Sin P}
      {FoldL Sin Fun Init Sout}
   end
   P
end

% 1.2. Port object without internal state
declare
fun {NewPortObject2 Proc}
   P
in
   thread Sin in
      {NewPort Sin P}
      for Msg in Sin do {Proc Msg} end
   end
   P
end

% Send starttimer(T Pid) message, return message sent after T milliseconds
declare
fun {Timer}
   {NewPortObject2
    proc {$ Msg}
       case Msg of starttimer(T Pid) then
	  thread {Delay T} {Send Pid stoptimer} end
       end
    end}
end

% 3.1 Controller agent
declare
fun {Controller Init}
   Tid = {Timer}
   Cid = {NewPortObject Init
	  fun {$ state(Motor F Lid) Msg}
	     case Motor
	     of running then
		case Msg
		of stoptimer then
		   {Send Lid 'at'(F) }
		   state(stopped F Lid)
		end
	     [] stopped then
		case Msg
		of step(Dest) then
		   if F==Dest then
		      state(stopped F Lid)
		   elseif F < Dest then
		      {Send Tid starttimer(1000 Cid)}
		      state(running F+1 Lid)
		   else
		      {Send Tid starttimer(1000 Cid)}
		      state(running F-1 Lid)
		   end
		end
	     end
	  end}
in Cid end

% 3.2 Floor agent
declare
fun {Floor Num Init Lifts}
   Tid= {Timer}
   Fid= {NewPortObject Init
	 fun {$ state(Called) Msg}
	    case Called
	    of notcalled then Lran in
	       case Msg
	       of arrive(Ack) then
		  {Browse 'Lift at floor '#Num#': open doors'}
		  {Send Tid starttimer(2000 Fid)}
		  state(doorsopen(Ack))
	       [] call then
		  {Browse 'Floor '#Num#' calls a lift!'}
		  Lran=Lifts.(1+{OS.rand} mod {Width Lifts})
		  {Send Lran call(Num)}
		  state(called)
	       end
	    [] called then
	       case Msg
		  of arrive(Ack) then
		     {Browse 'Lift at floor'#Num#': open doors'}
		     {Send Tid starttimer(2000 Fid)}
		     state(doorsopen(Ack))
		  [] call then
		     state(called)
		  end
	    [] doorsopen(Ack) then
		  case Msg
		  of stoptimer then
		     {Browse 'Lift at floor '#Num#': close doors'}
		     Ack=unit
		     state(notcalled)
		  [] arrive(A) then
		     A = Ack
		     state(doorsopen(Ack))
		  [] call then
		     state(doorsopen(Ack))
		  end
	       end
	    end}
in Fid end

% 3.3 Lift agent (with schedule function)
declare
fun {ScheduleLast L N}
   if L\=nil andthen {List.last L} == N then L
   else {Append L [N]} end
end

fun {Lift Num Init Cid Floors}
   {NewPortObject Init
    fun {$ state(Pos Sched Moving) Msg}
       case Msg
       of call(N) then
	  {Browse 'Lift '#Num#' needed at floor '#N}
	  if N==Pos andthen {Not Moving} then
	     {Browse 'At '#N#' floor!'} 
	     {Wait {Send Floors.Pos arrive($)}}
	     state(Pos Sched false)
	  else Sched2 in
	     Sched2={ScheduleLast Sched N}
	     if {Not Moving} then
		{Send Cid step(N)} end
	     state(Pos Sched2 true)
	  end
       [] 'at'(NewPos) then
	  {Browse 'Lift '#Num#' at floor '#NewPos}
	  case Sched
	  of S|Sched2 then
	     if NewPos==S then 
		{Wait {Send Floors.S arrive($)}}
		if Sched2==nil then
		   state(NewPos nil false)
		else
		   {Send Cid step(Sched2.1)}
		   state(NewPos Sched2 true)
		end
	     else
		{Send Cid step(S)}
		state(NewPos Sched Moving)
	     end
	  end
       end
    end}
  end

% 3.4 Building with FN floors and LN lifts
declare
proc {Building FN LN ?Floors ?Lifts}
   Lifts={MakeTuple lifts LN}
   for I in 1..LN do Cid in
      Cid= {Controller state(stopped 1 Lifts.I)}
      Lifts.I={Lift I state(1 nil false) Cid Floors}
   end
   Floors={MakeTuple floors FN}
   for I in 1..FN do
      Floors.I={Floor I state(notcalled) Lifts}
   end
end

/*

% Exercise: run the lift control system with various messages
declare F L in
{Building 10 2 F L}

{Send F.9 call}

{Delay 300}
{Send F.5 call}
{Send L.1 call(4)}
{Send L.2 call(1)}
%{Delay 5000}
%{Send L.1 call(3)}
%{Send L.2 call(3)}

*/

%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%
